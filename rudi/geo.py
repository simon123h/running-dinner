import math
try:
    from geopy.exc import GeocoderTimedOut
    from geopy.geocoders import Nominatim
except ImportError:
    raise ImportError(
        'Module \'geopy\' required.\nPlease install it via \'pip3 install --user geopy\'')

# Initialize geocoder
geolocator = Nominatim(user_agent="nominatim_testing")


def adress2coords(adress):
    """ Geocodes the adress of a location (string) to a coordinate pair """
    try:
        location = geolocator.geocode(adress)
        if location is None:
            print("Could not geocode adress:", adress)
            return None
        return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        return adress2coords(adress)


def spatial_distance(coords1, coords2):
    """ Calculates the spatial distance between too coordinate pairs """
    return math.sqrt(math.pow(coords1[0]-coords2[0], 2) + math.pow(coords1[1]-coords2[1], 2))
    # TODO: use the following implementation for actual coordinates
    latitude = math.radians(coords1[0] - coords2[0])
    longitude = math.radians(coords1[1] - coords2[1])
    earthRadius = 6371  # kilometers
    a = math.sin(latitude/2) * math.sin(latitude/2) + math.cos(math.radians(coords1[0])) * math.cos(
        math.radians(coords2[0])) * math.sin(longitude/2) * math.sin(longitude/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = earthRadius * c
    return dist
