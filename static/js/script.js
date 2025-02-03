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

// ADDING RECOMMENDATIONS TO MAP

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

// Populate category filter dropdown with fetched categories
const populateCategoryFilter = (categories) => {
    const categorySelect = document.getElementById("categorySelect");
    categorySelect.innerHTML = '<option value="">Select a category</option>'; // Reset options
    categories.forEach(category => {
        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });
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

// Function to add markers to the map
const addMarkers = (recommendations) => {
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
};

// Fetch initial recommendations and categories when the page loads
document.addEventListener("DOMContentLoaded", () => {
    fetchRecommendations();
    fetchCategories();
});

// Update the distance output as the slider changes
distanceSlider.addEventListener('input', () => {
    distanceOutput.textContent = `${distanceSlider.value} km`;
});

// Apply Filters on filter form submission
document.getElementById('filterForm').addEventListener('submit', (event) => {
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
