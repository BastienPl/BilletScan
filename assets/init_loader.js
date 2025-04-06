window.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('init-loader');
    
    const checkInterval = setInterval(() => {
        const app = document.getElementById('_dash-app-content');
        if (app && app.innerHTML.trim() !== '') {
            if (loader) {
                loader.style.display = 'none'; // Cache le splash
            }
            clearInterval(checkInterval);
        }
    }, 100);
    document.body.style.overflow = 'auto';
});
