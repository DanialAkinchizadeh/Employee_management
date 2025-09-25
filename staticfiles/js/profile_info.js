// Fade in elements when they come into view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate__animated', 'animate__fadeInUp');
        }
    });
});

document.querySelectorAll('.project-card, .about, .footer').forEach(section => {
    observer.observe(section);
});
const toast = document.getElementById('myToast');
const closeBtn = toast.querySelector('.close-btn');

const showMs = 3000; // مدت نمایش پیام (۳ ثانیه)

// نمایش پیام
function showToast() {
  toast.classList.add('show');
  setTimeout(() => {
    hideToast();
  }, showMs);
}

// مخفی‌سازی پیام
function hideToast() {
  toast.classList.remove('show');
  toast.classList.add('hide');
  setTimeout(() => {
    if (toast.parentElement) toast.parentElement.removeChild(toast);
  }, 400);
}

// اجرای اولیه
showToast();

// دکمه بستن
closeBtn.addEventListener('click', () => {
  hideToast();
});
