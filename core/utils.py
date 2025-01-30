import requests

def get_lat_long(address, api_key):
    """
    Get the latitude and longitude for a given address using the OpenCage Geocoder API.

    Args:
        address (str): The address to be geocoded (e.g., "1600 Pennsylvania Ave, Washington, DC").
        api_key (str): The OpenCage API key for authentication.

    Returns:
        tuple: A tuple containing the latitude and longitude of the given address.
               If the address is valid and the request is successful, returns (lat, lng).
               If the address is invalid or there is an error with the API, returns (None, None).

    Raises:
        requests.exceptions.RequestException: If there is a network error, a timeout, or any issue
                                              with the API request.

    Example:
        >>> get_lat_long("1600 Pennsylvania Ave, Washington, DC", "YOUR_API_KEY")
        (38.8977, -77.0365)

    Notes:
        - The OpenCage API returns a list of results, and this function extracts the coordinates
          from the first result in the list. It assumes that the first result is the most accurate.
        - Ensure that the address provided is correctly formatted to maximize the accuracy of the result.
        - If the OpenCage API quota is exceeded, or if the address cannot be geocoded, the function
          will return (None, None) and print an error message.
    """
    url = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['status']['code'] == 200:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        print(f"Error: {data['status']['message']}")
        return None, None
