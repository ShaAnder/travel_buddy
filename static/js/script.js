// --- QUERY SELECTORS / VARS --- //
const headerToggleBtn = document.querySelector(".header-toggle");
const header = document.querySelector("#header");
const navLinks = document.querySelectorAll("#nav a");

let locationModal, map, userMarker

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
        locationModal.show()
    }
});

// function to show location modal
function toggleLocationModal() {
    // Create the modal instance only once
    if (!locationModal) {
        locationModal = new bootstrap.Modal(document.getElementById("locationModal"));
    }

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
    let selectedCity = document.getElementById("citySelect").value;

    if (!selectedCity && !localStorage.getItem("userLocation")) {
        alert("Please select a city or use your current location.");
        return;
    }

    if (selectedCity) {
        let [lat, lng] = selectedCity.split(",");
        setLocation(parseFloat(lat), parseFloat(lng));  // Store selected city location
        updateMapLocation(parseFloat(lat), parseFloat(lng));  // Update map with new city location
    }

    closeModal();
}

// get our current location function
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            let lat = position.coords.latitude;
            let lng = position.coords.longitude;
            setLocation(lat, lng);  // Store current location
            updateMapLocation(lat, lng);  // Update map with current location
            closeModal();
        });
    } else {
        alert("Geolocation is not supported by your browser.");
    }
}


// MAP INITIATION

// function to load our map script
function loadMapScript(callback) {
    // if google maps API is loaded, initialize
    if (typeof google !== 'undefined' && google.maps) {
        callback();
    } else {
        // Try again in 100ms
        setTimeout(() => loadMapScript(callback), 100);
    }
}

// Update map location dynamically without reload
function updateMapLocation(newLat, newLng) {
    if (map && userMarker) {
        // Update map center to new location
        map.setCenter({ lat: newLat, lng: newLng });

        // Update marker position
        userMarker.setPosition({ lat: newLat, lng: newLng });

        // Optionally, store the new location in local storage
        localStorage.setItem("userLocation", JSON.stringify({ lat: newLat, lng: newLng }));
    } else {
        console.log("Map or marker is not initialized.");
    }
}


// Once the page is fully loaded, load the map
document.addEventListener('DOMContentLoaded', () => {
    loadMapScript(initMap);  // Wait until Google Maps API is ready
});

