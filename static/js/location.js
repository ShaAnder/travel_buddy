
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
function showLocationModal() {
    // create the new bootstrap modal using our modal id
    let locationModal = new bootstrap.Modal(document.getElementById("locationModal"));
    // show it
    locationModal.show();
}

// set our location in local storage
function setLocation(lat, lng) {
    localStorage.setItem("userLocation", JSON.stringify({ lat, lng }));
}

// change our city function
function changeCity() {
    // selec our city and get the value
    let selectedCity = document.getElementById("citySelect").value;
    // if we get a city
    if (selectedCity) {
        // get the lat /lng of the city
        let [lat, lng] = selectedCity.split(",");
        // set the location
        setLocation(lat, lng);
        // update our map
        updateMap(parseFloat(lat), parseFloat(lng));
    }
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
                // set the location, update the map
                setLocation(lat, lng);
                updateMap(lat, lng);
            },
            // if we get an error have them select a city
            () => alert("Geolocation failed. Please select a city.")
        );
    } else {
        // alert if they cannot use geolocate with their browser
        alert("Geolocation is not supported by your browser.");
    }
}