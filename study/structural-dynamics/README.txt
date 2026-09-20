Structural Dynamics & Aeroelasticity

구성: 7개 챕터, 20개 본문 글, 전체 목차 페이지.
영어 제목 · 한국어 설명 · 수식 · 한 줄 요약 · 이전/다음 글 링크.

바로 확인하기

압축을 푼 뒤 structural-dynamics/index.html을 브라우저에서 여세요.
각 소챕터 번호를 누르면 해당 글로 이동합니다.
넓은 화면에서는 왼쪽에 전체 글 목록, 오른쪽에 현재 글의 목차가 표시됩니다.
작은 화면에서는 Series Navigation을 펼쳐 전체 목록을 볼 수 있습니다.

GitHub 블로그에 넣기

1. structural-dynamics 폴더 전체를 기존 블로그의 study 폴더에 넣습니다.
   목차 위치: study/structural-dynamics/index.html

2. 블로그 최상위 index.html의 Study Notes 목록에서 Aerodynamics와 같은
   수준에 다음 링크를 추가합니다.

   <a href="study/structural-dynamics/">Structural Dynamics &amp; Aeroelasticity</a>

3. 기존 Study Notes 목록 파일이 다른 폴더에 있으면 링크의 상대경로를 맞춥니다.
   HTML, CSS, JavaScript, example 폴더를 함께 업로드해야 합니다.

목차

1. Fundamentals
   1.1 Vibration, Mass, Stiffness, and Damping
   1.2 Degrees of Freedom and Equations of Motion
2. Free Vibration
   2.1 Undamped Free Vibration
   2.2 Damped Free Vibration
3. Forced Vibration
   3.1 Harmonic Response and Resonance
   3.2 Base Excitation and Vibration Isolation
   3.3 Transient Response
4. Multi-Degree-of-Freedom Systems
   4.1 Coupled Equations and Matrix Form
   4.2 Natural Frequencies and Mode Shapes
   4.3 Modal Analysis
5. Continuous Systems and Beam Vibration
   5.1 Continuous Systems and Rod Vibration
   5.2 Euler–Bernoulli Beam Theory
   5.3 Beam Natural Frequencies and Mode Shapes
   5.4 Modal Response of Beams
6. Structural Analysis Methods
   6.1 Energy Methods and Equivalent Models
   6.2 Finite Element Method
   6.3 Response Analysis and Verification
7. Aeroelasticity and Flutter
   7.1 Aeroelastic Coupling and Static Stability
   7.2 Typical Section and Unsteady Aerodynamics
   7.3 Flutter Analysis and Stability Prediction

본문과 수식

1~6장은 첨부된 진동·구조동역학 원고를 바탕으로 구성했습니다.
7장은 공탄성 결합, 정적 Divergence, Typical section, 비정상 공기력,
Flutter 고유치 해석을 세 글로 연결하여 추가했습니다.
필요성은 본문 도입에서 설명하며, 제목은 영어의 개념 이름을 사용합니다.

수식은 MathML을 사용하므로 외부 수식 스크립트 다운로드가 필요 없습니다.
각 MathML annotation에는 편집에 참고할 LaTeX 표현이 들어 있습니다.
폭이 넓은 수식과 표는 해당 영역을 가로로 스크롤할 수 있습니다.

플러터 예시 재현하기

flutter-analysis/example/flutter_example.py가 본문 7.3의 계산 코드입니다.
Python에 numpy, scipy, matplotlib을 설치한 뒤 다음 명령을 실행합니다.

   python flutter_example.py

결과 파일은 계산 코드와 같은 폴더에 생성됩니다.
   flutter-results.json  : 경계 속도, 주파수, 일부 속도의 고유치 결과
   flutter-sweep.csv     : 추적한 두 진동 Mode의 속도별 고유치와 감쇠비
   flutter-stability.svg : 본문에 사용하는 주파수·감쇠비 그림
   flutter-stability.png : 같은 그림의 PNG 파일

입력은 본문에 명시한 교육용 Strip이며 특정 항공기의 측정값이 아닙니다.
Wagner 모델은 약 55.72 m/s, Quasi-steady 모델은 약 31.00 m/s에서
Flutter를 예측합니다. 정적 Divergence 경계는 약 72.09 m/s입니다.
공기력의 적용 가정과 각 모델의 차이는 7.2와 7.3 본문에 설명했습니다.
