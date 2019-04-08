from math import sqrt, pow
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
        return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        return adress2coords(adress)


def spatial_distance(coords1, coords2):
    """ Calculates the spatial distance between too coordinate pairs """
    # TODO: is this a sane implementation?
    return sqrt(pow(coords1[0]-coords2[0], 2) + pow(coords1[1]-coords2[1], 2))
