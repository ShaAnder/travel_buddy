import requests
from travel_buddy.settings import GOOGLE_API

def get_irish_cities():
    """
    Fetch a list of cities in Ireland using the Google Places API.

    Args:
        api_key (str): Your Google Maps API key.

    Returns:
        list: A list of city names and their lat/lng.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": "cities in Ireland",
        "key": GOOGLE_API
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "OK":
        # Filter relevant information (name, lat, lng) from the response
        cities = [{"name": place["name"], "lat": place["geometry"]["location"]["lat"], "lng": place["geometry"]["location"]["lng"]} for place in data["results"]]
        return cities
    else:
        return []
    
def get_lat_long(address):
    """
    Get latitude and longitude for a given address using Google Maps Geocoding API.

    Args:
        address (str): The address to geocode.
        api_key (str): Your Google Maps API key.

    Returns:
        tuple: Latitude and longitude of the address.
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "OK":
        # Extract latitude and longitude
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        return None, None