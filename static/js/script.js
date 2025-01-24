(function init() {
// INIT HEADER TOGGLE //
handleHeaderToggle = () => {
    // find our header element and adds a toggle
    document.querySelector("#header").classList.toggle("header-show");
    headerToggleBtn.classList.toggle("bi-list");
    headerToggleBtn.classList.toggle("bi-x");
    // Hide the nav bar
    document.querySelectorAll("#nav a").forEach((nav) => {
        nav.addEventListener("click", () => {
        if (document.querySelector(".header-show")) {
            handleHeaderToggle();
        }
        });
    });
};

})