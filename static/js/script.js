// --- QUERY SELECTORS / VARS --- //
const headerToggleBtn = document.querySelector(".header-toggle");
const header = document.querySelector("#header");
const navLinks = document.querySelectorAll("#nav a");

// --- TOGGLE HEADER --- //

if (headerToggleBtn && header) { 
    const handleHeaderToggle = () => {
        header.classList.toggle("header-show");
        headerToggleBtn.classList.toggle("bi-list");
        headerToggleBtn.classList.toggle("bi-x");
    };

    // Attach click event listener to the toggle button
    headerToggleBtn.addEventListener("click", handleHeaderToggle);

    // Close the nav bar if a nav link is clicked (when open)
    navLinks.forEach((nav) => {
        nav.addEventListener("click", () => {
            if (header.classList.contains("header-show")) {
                handleHeaderToggle();
            }
        });
    });
}