// --- QUERY SELECTORS / VARS --- //
const headerToggleBtn = document.querySelector(".header-toggle");
const header = document.querySelector("#header");
const navLinks = document.querySelectorAll("#nav a");

// --- TOGGLE HEADER --- //

/**
 * Toggles the header visibility and button icons.
 */
if (headerToggleBtn && header) {
    const handleHeaderToggle = () => {
        header.classList.toggle("header-show");
        headerToggleBtn.classList.toggle("bi-list");
        headerToggleBtn.classList.toggle("bi-x");
    };

    // Attach click event listener to the toggle button
    headerToggleBtn.addEventListener("click", handleHeaderToggle);

    /**
     * Closes the navigation bar if a nav link is clicked when open.
     */
    navLinks.forEach((nav) => {
        nav.addEventListener("click", () => {
            if (header.classList.contains("header-show")) {
                handleHeaderToggle();
            }
        });
    });
}

// LOCATION TRACKING //


// add an event listener for dom load
document.addEventListener("DOMContentLoaded", function () {
    // check if our user has a location
    let userHasLocation = localStorage.getItem("userLocation");
    // if no location show our location modal
    if (!userHasLocation) {
        showLocationModal();
    }
});

// function to show location modal
function toggleLocationModal() {
    let locationModal = new bootstrap.Modal(document.getElementById("locationModal"));
    
    // Toggle the modal (open if closed, close if open)
    if (locationModal._isShown) {
        locationModal.hide();  // Close the modal if it's already open
    } else {
        locationModal.show();  // Open the modal if it's closed
    }
}

// function to hide modal
function closeModal() {
    // get the instance of the modal
    let locationModal = bootstrap.Modal.getInstance(document.getElementById("locationModal"));
    // if open toggle to hide
    if (locationModal) {
        locationModal.hide();
    }
}

// set our location in local storage
function setLocation(lat, lng) {
    localStorage.setItem("userLocation", JSON.stringify({ lat, lng }));
}

// change our city function
function confirmLocation() {
    // selec our city and get the value
    let selectedCity = document.getElementById("citySelect").value;
    // if we don't get a city AND we don't have saved data
    if (!selectedCity && !localStorage.getItem("userLocation")) {
        // notify user they need to select a city or use their location
        alert("Please select a city or use your current location");
        return;
    }
    // if we get a city
    if (selectedCity) {
        // get the lat /lng of the city
        let [lat, lng] = selectedCity.split(",");
        // set the location
        setLocation(parseFloat(lat), parseFloat(lng));
    }
    // and close our modal
    closeModal()
}

// get our current location function
function getCurrentLocation() {
    // if we have a navigator geolocation
    if (navigator.geolocation) {
        // get the current position lat / long
        navigator.geolocation.getCurrentPosition(
            (position) => {
                let lat = position.coords.latitude;
                let lng = position.coords.longitude;
                // set the location, update the map, close modal
                setLocation(lat, lng);
                closeModal();
            },
            // if we get an error have them select a city
            () => alert("Geolocation failed. Please select a city.")
        );
    } else {
        // alert if they cannot use geolocate with their browser
        alert("Geolocation is not supported by your browser.");
    }
}
