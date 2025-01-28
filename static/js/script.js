// --- QUERY SELECTORS / VARS --- //
const headerToggleBtn = document.querySelector(".header-toggle");
const header = document.querySelector("#header");
const navLinks = document.querySelectorAll("#nav a");

// --- HANDLE ERRORS --- //

// Handle error for trying to edit another users page gives users an
// unauthorized message and returns them to their previous page
document.addEventListener('DOMContentLoaded', function() {
    // Check if the specific error message for editing profile exists
    const errorMessage = document.getElementById('edit-profile-error-message');

    if (errorMessage) {
        // Get the actual error message text
        const errorText = document.getElementById('edit-profile-error-text').textContent;
        
        // Log the error message to the console for debugging
        console.error('Edit Profile Error: ' + errorText);

        // Set a brief delay (e.g., 3 seconds) before redirecting
        setTimeout(function() {
            window.history.back();  // Go back to the previous page
        }, 3000);  // 3000 milliseconds = 3 seconds
    }
});


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