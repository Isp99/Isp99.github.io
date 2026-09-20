"""Chapter 7.3: linear typical-section flutter, SI units.

Run: python flutter_example.py
Dependencies: numpy, scipy, matplotlib.
The 1 m span strip uses h positive down, alpha positive nose up.
Aerodynamics: incompressible thin-airfoil theory, noncirculatory loads,
and either instantaneous circulation or the two-state Jones/Wagner model.
This is an educational model; parameters are not measurements of an aircraft.
"""
from pathlib import Path
import csv
import json
import numpy as np
from scipy.linalg import eig
from scipy.optimize import brentq, linear_sum_assignment

B = 0.5                 # semichord, m
A = -0.2                # elastic axis: A*B aft of midchord
SPAN = 1.0              # strip span, m
RHO = 1.225             # kg/m^3
MASS = 20.0             # kg
INERTIA = 1.2           # kg m^2 about elastic axis
S_ALPHA = 1.0           # mass first moment, kg m (CG aft)
KH = 8000.0            # N/m
KALPHA = 3000.0        # N m/rad
CH = 8.0               # N s/m
CALPHA = 1.2           # N m s/rad
M = np.array([[MASS, S_ALPHA], [S_ALPHA, INERTIA]])
C = np.diag([CH, CALPHA])
K = np.diag([KH, KALPHA])
ELL = B * (A + 0.5)    # AC ahead of elastic axis, m
D = B * (0.5 - A)      # three-quarter-chord aft of elastic axis, m
P = np.array([-1.0, ELL])
WQ = np.array([0.0, 1.0])
WV = np.array([1.0, D])
JONES_C = np.array([0.165, 0.335])
JONES_EPS = np.array([0.0455, 0.3])
MU_A = np.pi * RHO * SPAN * B**2
# Q_a = A2*qdd + A1*qdot + A0*q + lag forces.
A2 = MU_A * np.array([[-1.0, A*B], [A*B, -B**2*(1/8 + A*A)]])
ME = M - A2


def state_matrix(speed, unsteady=True):
    """Return the 4x4 quasi-steady or 6x6 Wagner state matrix."""
    if speed < 0:
        raise ValueError("Speed must be nonnegative")
    gain = 2*np.pi*RHO*SPAN*B*speed
    direct = 1 - JONES_C.sum() if unsteady else 1.0
    a0 = gain*direct*np.outer(P, speed*WQ)
    a1 = gain*direct*np.outer(P, WV)
    a1 += MU_A*speed*np.array([[0.0, -1.0], [0.0, -D]])
    n = 6 if unsteady else 4
    matrix = np.zeros((n, n))
    matrix[:2, 2:4] = np.eye(2)
    matrix[2:4, :2] = -np.linalg.solve(ME, K-a0)
    matrix[2:4, 2:4] = -np.linalg.solve(ME, C-a1)
    if unsteady:
        matrix[2:4, 4:] = np.linalg.solve(ME, gain*np.outer(P, np.ones(2)))
        rates = JONES_EPS*speed/B
        matrix[4:, :2] = np.outer(JONES_C*rates, speed*WQ)
        matrix[4:, 2:4] = np.outer(JONES_C*rates, WV)
        matrix[4:, 4:] = -np.diag(rates)
    return matrix


def oscillatory_modes(speed, unsteady=True):
    values, vectors = eig(state_matrix(speed, unsteady))
    keep = values.imag > 1e-7
    return values[keep], vectors[:, keep]


def growth(speed, unsteady=True):
    # All eigenvalues matter: real divergence must not be ignored.
    return np.linalg.eigvals(state_matrix(speed, unsteady)).real.max()


def first_flutter(unsteady=True):
    grid = np.linspace(0.1, 70.0, 700)
    for lower, upper in zip(grid[:-1], grid[1:]):
        if growth(lower, unsteady) < 0 <= growth(upper, unsteady):
            speed = brentq(lambda u: growth(u, unsteady), lower, upper, xtol=1e-11)
            values = np.linalg.eigvals(state_matrix(speed, unsteady))
            critical = values[np.argmax(values.real)]
            assert abs(critical.imag) > 1e-5, "First instability is static, not flutter"
            return speed, abs(critical.imag)
    raise RuntimeError("No flutter crossing in search interval")


def sweep(speeds):
    """Track branches using mass-weighted structural displacement correlation."""
    result = []
    previous = None
    for speed in speeds:
        values, vectors = oscillatory_modes(speed)
        assert len(values) == 2, "This sweep expects two oscillatory branches"
        shapes = vectors[:2, :]
        if previous is None:
            order = np.argsort(values.imag)
        else:
            numerator = np.abs(previous.conj().T @ M @ shapes)**2
            prev_norm = np.diag(previous.conj().T @ M @ previous).real
            new_norm = np.diag(shapes.conj().T @ M @ shapes).real
            mac = numerator / np.outer(prev_norm, new_norm)
            rows, order = linear_sum_assignment(1-mac)
            assert np.array_equal(rows, np.arange(2))
        previous = shapes[:, order]
        result.append(values[order])
    return np.array(result)


def main(out=None):
    out = Path(out) if out else Path(__file__).resolve().parent
    out.mkdir(parents=True, exist_ok=True)
    assert np.linalg.eigvalsh(M).min() > 0
    assert np.linalg.eigvalsh(ME).min() > 0
    uf, wf = first_flutter()
    uqs, wqs = first_flutter(False)
    ud = np.sqrt(KALPHA/(0.5*RHO*(2*B*SPAN)*2*np.pi*ELL))
    # At zero frequency the Wagner lags restore steady circulation.
    u = 25.0
    matrix = state_matrix(u)
    condensed = matrix[:4,:4] - matrix[:4,4:] @ np.linalg.solve(matrix[4:,4:],matrix[4:,:4])
    np.testing.assert_allclose(condensed, state_matrix(u,False), atol=1e-11)
    # Verify energy is conserved by the undamped no-flow effective model.
    q = np.array([0.002, 0.004]); v = np.array([0.1, -0.03])
    acceleration = np.linalg.solve(ME, -K@q)
    assert abs(v@ME@acceleration + v@K@q) < 1e-10
    assert growth(uf-.1) < 0 < growth(uf+.1)
    assert uf < ud
    speeds = np.linspace(0.1, 62, 500)
    values = sweep(speeds)
    table = []
    for u in [20.0, 40.0, uf, 60.0]:
        eigs, _ = oscillatory_modes(u)
        reference = values[np.argmin(np.abs(speeds-u)), 1]
        ev = eigs[np.argmin(np.abs(eigs-reference))]
        table.append(dict(speed=u, sigma=float(ev.real), omega=float(ev.imag),
                          zeta=float(-ev.real/abs(ev))))
    report = dict(wagner_flutter_speed=uf, wagner_flutter_omega=wf,
                  quasisteady_flutter_speed=uqs, quasisteady_flutter_omega=wqs,
                  divergence_speed=ud, flutter_reduced_frequency=wf*B/uf,
                  table_branch='Mode 2, tracked from the higher-frequency mode at low speed', rows=table)
    (out/'flutter-results.json').write_text(json.dumps(report, indent=2))
    with (out/'flutter-sweep.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['U_m_per_s','sigma_1_per_s','omega_1_rad_per_s','zeta_1',
                         'sigma_2_per_s','omega_2_rad_per_s','zeta_2'])
        for u, modes in zip(speeds, values):
            writer.writerow([u]+[x for ev in modes for x in (ev.real,ev.imag,-ev.real/abs(ev))])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':11, 'font.family':'DejaVu Sans',
                         'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    fig, axes = plt.subplots(2,1,figsize=(8.5,6.8),sharex=True,constrained_layout=True)
    for i,color in enumerate(['#506171','#ab592b']):
        axes[0].plot(speeds,values[:,i].imag,color=color,lw=2,label=f'Mode {i+1}')
        axes[1].plot(speeds,-values[:,i].real/np.abs(values[:,i]),color=color,lw=2)
    for ax in axes:
        ax.axvline(uf,color='#333333',lw=1,ls='--')
        ax.grid(axis='y',color='#e8e8e8',lw=.7)
    axes[0].legend(frameon=False,loc='upper right')
    axes[0].set_ylabel('Frequency, omega (rad/s)')
    axes[0].set_title('Typical-section stability with Wagner aerodynamics',loc='left',pad=15)
    axes[1].axhline(0,color='#777777',lw=.9)
    axes[1].set_ylabel('Modal damping ratio, zeta')
    axes[1].set_xlabel('Flow speed, U (m/s)')
    axes[1].text(uf+1,.01,f'Flutter\n{uf:.2f} m/s',va='bottom',fontsize=10)
    axes[1].set_xlim(0,62)
    fig.savefig(out/'flutter-stability.svg')
    fig.savefig(out/'flutter-stability.png', dpi=160)
    plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else None)
