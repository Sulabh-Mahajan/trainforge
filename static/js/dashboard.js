const sidebarToggle = document.getElementById("sidebarToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("sidebarOverlay");

sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("sidebar-open");
    overlay.classList.toggle("active");
});

overlay.addEventListener("click", () => {
    sidebar.classList.remove("sidebar-open");
    overlay.classList.remove("active");
});

document.addEventListener('DOMContentLoaded', function() {
    const clientToast = document.getElementById('clientAddedToast');
    if (clientToast) {
        setTimeout(function() {
            clientToast.style.transition = 'opacity 0.5s ease';
            clientToast.style.opacity = '0';
            setTimeout(function() {
                clientToast.remove();
            }, 500);
        }, 1000);
    }
});



