// --- QUERY SELECTORS / VARS --- //
const headerToggleBtn = document.querySelector(".header-toggle");
const header = document.querySelector("#header");
const navLinks = document.querySelectorAll("#nav a");

let locationModal
let map
let userMarker
let markers = []

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


// ADDING RECOMMENDATIONS TO MAP

async function fetchRecommendations(filterCriteria = null) {
    try {
        const response = await fetch('/api/recommendations/');
        if (response.ok) {
            const recommendations = await response.json();

            // If filter criteria is provided, apply it
            const filteredRecommendations = filterCriteria ? filterRecommendations(recommendations, filterCriteria) : recommendations;

            // Clear the existing markers before adding new ones
            clearMarkers();

            // Add markers to the map
            addMarkers(filteredRecommendations);
        } else {
            console.log("Failed to fetch recommendations.");
        }
    } catch (error) {
        console.error("Error fetching recommendations:", error);
    }
}

function filterRecommendations(recommendations, filterCriteria) {
    return recommendations.filter(recommendation => {
        const { latitude, longitude, category } = recommendation;
        let isValid = true;

        // Filter by distance
        const distance = haversine(userMarker.position.lat(), userMarker.position.lng(), latitude, longitude);
        if (filterCriteria.distance && distance > filterCriteria.distance) {
            isValid = false;
        }

        // Filter by category if specified
        if (filterCriteria.category && category !== filterCriteria.category) {
            isValid = false;
        }

        return isValid;
    });
}

// Function to clear existing markers
function clearMarkers() {
    // Loop through existing markers and remove them from the map
    markers.forEach(marker => {
        marker.setMap(null);
    });
    markers = []; // Clear the markers array
}

// Function to add markers to the map
function addMarkers(recommendations) {
    recommendations.forEach(recommendation => {
        const { latitude, longitude, title } = recommendation;

        // Create marker for each recommendation
        const marker = new google.maps.Marker({
            position: { lat: latitude, lng: longitude },
            map: map,
            title: title
        });

        // Optionally, add info windows or click events to markers
        const infoWindow = new google.maps.InfoWindow({
            content: `<h5>${title}</h5>`
        });

        marker.addListener("click", () => {
            infoWindow.open(map, marker);
        });

        // Add marker to the markers array for future removal
        markers.push(marker);
    });
}


document.addEventListener("DOMContentLoaded", function() {
    fetchRecommendations();
});