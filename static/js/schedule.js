// Sidebar toggle
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');

document.getElementById('sidebarToggle')?.addEventListener('click', () => {
    sidebar.classList.toggle('sidebar-open');
    overlay.classList.toggle('active');
});

overlay?.addEventListener('click', () => {
    sidebar.classList.remove('sidebar-open');
    overlay.classList.remove('active');
});