window.addEventListener('DOMContentLoaded', () => {
    const observer = new MutationObserver(() => {
        const app = document.getElementById('_dash-app-content');
        if (app && app.innerHTML.trim() !== '') {
            const loader = document.getElementById('init-loader');
            if (loader) {
                loader.style.display = 'none';
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
