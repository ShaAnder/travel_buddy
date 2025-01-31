import requests
from travel_buddy.settings import GEONAME_API

def get_irish_cities():
    """
    Fetch a list of major cities in Ireland using the GeoNames API.
    
    Args:
        username (str): Your GeoNames API username.

    Returns:
        list: A list of dictionaries containing city names and their lat/lng.
    """
    url = "http://api.geonames.org/searchJSON"
    params = {
        "q": "",  # Empty query to return all
        "country": "IE",  # Ireland
        "featureClass": "P",  # Populated place
        "maxRows": 50,  # Adjust this if needed
        "username": GEONAME_API
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "geonames" in data:
        return [{"name": city["name"], "lat": city["lat"], "lng": city["lng"]} for city in data["geonames"]]
    return []