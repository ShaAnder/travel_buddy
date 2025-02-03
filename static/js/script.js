// --- QUERY SELECTORS / VARS --- //
// Get references to the header toggle button, header, and nav links
const headerToggleBtn = document.querySelector(".header-toggle");
const header = document.querySelector("#header");
const navLinks = document.querySelectorAll("#nav a");

// Get references to the distance slider and output for user distance input
const distanceSlider = document.getElementById('distanceSlider');
const distanceOutput = document.getElementById('distanceOutput');

// Initialize modals and markers as undefined
let locationModal;
let filterModal;
let map;
let userMarker;
let markers = [];

/**
 * Initialize the map and set the user's initial location.
 */
function initMap() {
    // Default location (e.g., New York)
    const initialLocation = { lat: 40.7128, lng: -74.0060 };

    // Initialize map
    map = new google.maps.Map(document.getElementById("map"), {
        center: initialLocation,
        zoom: 12,
    });

    // Create a marker at the initial location
    userMarker = new google.maps.Marker({
        position: initialLocation,
        map: map,
        title: "You are here",
        icon: {
            url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"  // Set the marker icon to a blue dot
        }
    });

    // Call update function if needed (e.g., getting user location from storage)
    updateMapLocationFromLocalStorage();
}

/**
 * Updates the map's location based on stored user data.
 */
function updateMapLocationFromLocalStorage() {
    const storedLocation = localStorage.getItem("userLocation");
    if (storedLocation) {
        const { lat, lng } = JSON.parse(storedLocation);
        map.setCenter({ lat, lng });
        userMarker.setPosition({ lat, lng });
    }
}

// --- TOGGLE HEADER --- //

// Toggle the header visibility and icon state when clicked
if (headerToggleBtn && header) {
    const handleHeaderToggle = () => {
        header.classList.toggle("header-show");
        headerToggleBtn.classList.toggle("bi-list");
        headerToggleBtn.classList.toggle("bi-x");
    };

    // Add event listener for the header toggle button
    headerToggleBtn.addEventListener("click", handleHeaderToggle);
    
    // Add event listener for nav links to close the header when clicked
    navLinks.forEach(nav => {
        nav.addEventListener("click", () => {
            if (header.classList.contains("header-show")) {
                handleHeaderToggle();
            }
        });
    });
}

// LOCATION TRACKING //

// Check if user has a stored location, show modal if not
document.addEventListener("DOMContentLoaded", () => {
    const userHasLocation = localStorage.getItem("userLocation");
    if (!userHasLocation) {
        locationModal.show();
    }
});

// Show or hide the location modal
const toggleLocationModal = () => {
    if (!locationModal) {
        locationModal = new bootstrap.Modal(document.getElementById("locationModal"));
    }
    if (locationModal._isShown) {
        locationModal.hide();
    } else {
        locationModal.show();
    }
};

// Show or hide the filter modal
const toggleFilterModal = () => {
    if (!filterModal) {
        filterModal = new bootstrap.Modal(document.getElementById('filterModal'));
    }

    if (filterModal._isShown) {
        filterModal.hide();
    } else {
        filterModal.show();
    }
};

// Close the location modal
const closeModal = () => {
    const locationModal = bootstrap.Modal.getInstance(document.getElementById("locationModal"));
    if (locationModal) {
        locationModal.hide();
    }
};

// Store the user's location in localStorage
const setLocation = (lat, lng) => {
    localStorage.setItem("userLocation", JSON.stringify({ lat, lng }));
};

// Handle location confirmation by selected city or current location
const confirmLocation = () => {
    const selectedCity = document.getElementById("citySelect").value;
    if (!selectedCity && !localStorage.getItem("userLocation")) {
        alert("Please select a city or use your current location.");
        return;
    }

    if (selectedCity) {
        const [lat, lng] = selectedCity.split(",");
        setLocation(parseFloat(lat), parseFloat(lng));  // Store selected city location
        updateMapLocation(parseFloat(lat), parseFloat(lng));  // Update map with new city location
    }

    closeModal();
};

// Get the current location using the Geolocation API
const getCurrentLocation = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            setLocation(lat, lng);  // Store current location
            updateMapLocation(lat, lng);  // Update map with current location
            closeModal();
        });
    } else {
        alert("Geolocation is not supported by your browser.");
    }
};

// MAP INITIATION

// Load the Google Maps script and initialize the map
const loadMapScript = (callback) => {
    // if google maps API is loaded, initialize
    if (typeof google !== 'undefined' && google.maps) {
        callback();
    } else {
        // Try again in 100ms
        setTimeout(() => loadMapScript(callback), 100);
    }
};

// Update map location dynamically without reload
const updateMapLocation = (newLat, newLng) => {
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
};

// Once the page is fully loaded, load the map
document.addEventListener('DOMContentLoaded', () => {
    loadMapScript(initMap);  // Wait until Google Maps API is ready
});

// Fetch recommendations from the server, apply filters if any
const fetchRecommendations = async (filterCriteria = null) => {
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
};

// Fetch categories from the server to populate the filter
const fetchCategories = async () => {
    try {
        const response = await fetch('/api/categories/');
        if (response.ok) {
            const categories = await response.json();
            populateCategoryFilter(categories);
        } else {
            console.log("Failed to fetch categories.");
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
};

// Modify this function to ensure the element exists
const populateCategoryFilter = (categories) => {
    const categorySelect = document.getElementById('categorySelect');
    
    if (categorySelect) {
        // Clear existing options
        categorySelect.innerHTML = '';

        // Populate the select dropdown with categories
        categories.forEach((category) => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            categorySelect.appendChild(option);
        });
    } else {
        console.error('Category select element not found!');
    }
};


// Filter recommendations based on selected criteria (distance, category)
const filterRecommendations = (recommendations, filterCriteria) => {
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
};

// Function to clear existing markers
const clearMarkers = () => {
    // Loop through existing markers and remove them from the map
    markers.forEach(marker => {
        marker.setMap(null);
    });
    markers = []; // Clear the markers array
};

/**
 * Adds markers to the map for each recommendation, hiding markers beyond a certain distance.
 * Also, populates the info window with additional details.
 * @param {Array} recommendations List of recommendations to create markers for.
 */
const addMarkers = (recommendations) => {
    // Maximum distance (in km) to show markers by default
    const maxDistance = 30; 

    recommendations.forEach(recommendation => {
        const { latitude, longitude, title, description, address } = recommendation;

        // Calculate the distance from the user's location
        const distance = haversine(userMarker.position.lat(), userMarker.position.lng(), latitude, longitude);

        // Skip markers that are beyond the maximum distance
        if (distance > maxDistance) return;

        // Create the marker
        const marker = new google.maps.Marker({
            position: { lat: latitude, lng: longitude },
            map: map,
            title: title,
        });

        // Create the content for the info window with additional details
        const infoContent = `
            <h5>${title}</h5>
            <p>${description}</p>
            <p><strong>Address:</strong> ${address}</p>
            <p><a href="https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}" target="_blank">Get Directions</a></p>
        `;

        const infoWindow = new google.maps.InfoWindow({
            content: infoContent
        });

        marker.addListener("click", () => {
            infoWindow.open(map, marker);
        });

        markers.push(marker);
    });
};

// Fetch initial recommendations and categories when the page loads
document.addEventListener("DOMContentLoaded", () => {
    fetchRecommendations();
    fetchCategories();
});

// Update the distance output as the slider changes
document.addEventListener("DOMContentLoaded", function() {
    const distanceSlider = document.getElementById('distanceSlider');
    const distanceOutput = document.getElementById('distanceOutput');

    // Check if both elements exist before trying to add event listener
    if (distanceSlider && distanceOutput) {
        distanceSlider.addEventListener('input', () => {
            distanceOutput.textContent = `${distanceSlider.value} km`;
        });
    } else {
        console.log("Required elements (distanceSlider or distanceOutput) not found!");
    }
});

// Apply Filters on filter form submission
document.addEventListener("DOMContentLoaded", function() {
    const filterForm = document.getElementById('filterForm');

    // Check if the filter form exists before adding the event listener
    if (filterForm) {
        filterForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const selectedCategory = document.getElementById('categorySelect').value;
            const selectedDistance = distanceSlider.value;

            // Build the filter criteria object
            const filterCriteria = {
                category: selectedCategory,
                distance: selectedDistance
            };

            // Fetch recommendations and apply filters
            fetchRecommendations(filterCriteria);

            // Close the modal after applying filters
            toggleFilterModal();
        });
    } else {
        console.log("Filter form not found!");
    }
});

/**
 * Haversine function to calculate distance between two points on the Earth.
 * @param {number} lat1 Latitude of first point.
 * @param {number} lon1 Longitude of first point.
 * @param {number} lat2 Latitude of second point.
 * @param {number} lon2 Longitude of second point.
 * @returns {number} Distance in kilometers.
 */
function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

/**
 * Converts degrees to radians.
 * @param {number} degrees Angle in degrees.
 * @returns {number} Angle in radians.
 */
function toRad(degrees) {
    return degrees * Math.PI / 180;
}

/**
 * Handles the splash screen timeout logic.
 */
function handleSplashScreen() {
    const splashScreen = document.getElementById('splash-screen');
    const homePage = document.getElementById('home-page');
    const travelText = document.getElementById('travel');
    const buddyText = document.getElementById('buddy');
    const leadText = document.querySelector('.lead');
    
    // Fade in Travel Buddy text
    setTimeout(() => {
        travelText.style.transition = "opacity 2s ease-in-out";
        buddyText.style.transition = "opacity 2s ease-in-out";
        leadText.style.transition = "opacity 2s ease-in-out";
        
        travelText.style.opacity = 1;
        buddyText.style.opacity = 1;
        leadText.style.opacity = 1;
    }, 500);

    // Show loader
    setTimeout(() => {
        splashScreen.style.transition = "opacity 1s ease-in-out";
        splashScreen.style.opacity = 0;

        // After splash fades out, hide it and show home page
        setTimeout(() => {
            splashScreen.style.display = 'none';
            homePage.style.display = 'flex';
        }, 1000); // Give enough time for the fade-out
    }, 2000); // Time before loader disappears
}

