import requests

def get_lat_long(address, api_key):
    """
    Get latitude and longitude for a given address using OpenCage API.
    """
    # Prepare the URL with the address and API key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}'

    # Send the GET request
    response = requests.get(url)
    data = response.json()

    # Check for a valid response
    if data['status']['code'] == 200:
        # Extract latitude and longitude from the first result
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        # Handle errors (e.g., invalid address)
        print(f"Error: {data['status']['message']}")
        return None, None