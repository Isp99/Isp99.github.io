(() => {
    const toc = document.querySelector('.page-toc');
    if (!toc || !('IntersectionObserver' in window)) return;
    const links = [...toc.querySelectorAll('a[href^="#"]')];
    const observer = new IntersectionObserver(entries => {
        for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            for (const link of links) {
                const active = link.hash === '#' + entry.target.id;
                link.classList.toggle('active', active);
                if (active) link.setAttribute('aria-current', 'location');
                else link.removeAttribute('aria-current');
            }
        }
    }, { rootMargin: '-5% 0px -75% 0px' });
    document.querySelectorAll('.article-section').forEach(section => observer.observe(section));
})();
