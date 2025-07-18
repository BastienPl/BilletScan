(function () {
    const loader = document.getElementById('init-loader');

    const hideLoader = () => {
        if (loader) {
            loader.style.transition = 'opacity 0.5s ease';
            loader.style.opacity = 0;
            setTimeout(() => loader.style.display = 'none', 500);
        }
    };

    const observer = new MutationObserver(() => {
        const app = document.getElementById('_dash-app-content');
        if (app && app.innerHTML.trim() !== '') {
            hideLoader();
            observer.disconnect();
        }
    });

    window.addEventListener('load', () => {
        observer.observe(document.body, { childList: true, subtree: true });
    });
    document.body.style.overflow = 'auto';
})();
