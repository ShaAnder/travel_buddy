"""
Module to interact with the Google Places and Geocoding APIs.

This module contains functions to get cities in Ireland using the Google
Places API and to get latitude and longitude for a given address using the
Google Maps Geocoding API.
"""
import requests
from travel_buddy.settings import GOOGLE_API


def get_irish_cities():
    """
    Fetch a list of cities in Ireland using the Google Places API.

    This function sends a request to the Google Places API to retrieve a list of
    cities in Ireland, along with their latitude and longitude coordinates.

    Args:
        None

    Returns:
        list: A list of dictionaries, each containing a city name and its
              latitude and longitude coordinates (lat, lng).
              Example: [{'name': 'Dublin', 'lat': 53.349805, 'lng': -6.26031}, ...]
        If the request is unsuccessful or no data is found, an empty list is returned.
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
        cities = [{
            "name": place["name"],
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"]} for place in data["results"]]
        return cities
    else:
        return []


def get_lat_long(address):
    """
    Get latitude and longitude for a given address using Google Maps Geocoding API.

    This function sends a request to the Google Geocoding API to retrieve the
    latitude and longitude coordinates for a specific address.

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: A tuple containing latitude and longitude of the address.
               Example: (53.349805, -6.26031)
        If the request is unsuccessful or no coordinates are found,
        (None, None) is returned.
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
