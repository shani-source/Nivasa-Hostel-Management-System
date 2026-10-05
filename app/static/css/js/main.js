const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

menuToggle.addEventListener("click", () => {
    navMenu.classList.toggle("active");
});
function toggleNotifications() {
    const dropdown = document.getElementById("notificationDropdown");

    if (!dropdown) return;

    dropdown.classList.toggle("show");
}

document.addEventListener("click", function(event) {

    const wrapper = document.querySelector(".notification-wrapper");
    const dropdown = document.getElementById("notificationDropdown");

    if (!wrapper || !dropdown) return;

    if (!wrapper.contains(event.target)) {
        dropdown.classList.remove("show");
    }
});