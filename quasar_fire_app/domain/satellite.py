import json

from quasar_fire_app.models.satellite import Satellite


def update_satellite(satellite_name, distance, message):
    """
    Update the distance from a satellite to the transmitter, 
    and the message received by it, given a satellite name.

    Args:
        - satellite_name (str): name of the satellite to filter by.
        - distance (float): distance from the transmitter to the satellite.
        - message (str): message received in the satellite.
    """
    satellite = Satellite.objects.get(name=satellite_name)

    satellite.distance_from_transmitter = distance
    satellite.message_received = json.dumps(message)
    satellite.save()


def get_all_satellites_info():
    """
    Retrieve all information about the satellites.
    
    Returns:
        QuerySet: List of satellites and their information.
    """
    return Satellite.objects.all()


def get_coordinates_by_satellite_name(satellite_name):
    """
    Retrieve the coordinates (X,Y) of a satellite, given a satellite name.

    Args:
        - satellite_name (str): name of the satellite to filter by.

    Returns:
        tuple(float, float): (X,Y) coordinates of the satellite.
    """
    return Satellite.objects.values_list(
        'x_position',
        'y_position'
    ).get(name=satellite_name)
