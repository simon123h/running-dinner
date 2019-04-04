from math import sqrt, pow


def adress2coords(adress):
    """ Geocodes the adress of a location (string) to a coordinate pair """
    # TODO: implement
    return (0, 0)


def spatial_distance(coords1, coords2):
    """ Calculates the spatial distance between too coordinate pairs """
    # TODO: is this a sane implementation
    return sqrt(pow(coords1[0]-coords2[0], 2) + pow(coords1[1]-coords2[1], 2))
