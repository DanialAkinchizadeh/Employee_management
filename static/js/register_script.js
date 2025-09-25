// Show loading screen initially and hide it after page load with a minimum delay
window.addEventListener('load', () => {
    const loading = document.getElementById('loading');
    setTimeout(() => {
        loading.style.opacity = '0';
        setTimeout(() => {
            loading.style.display = 'none';
        }, 500); // Fade out duration
    }, 2000); // Minimum 2 seconds display
});




