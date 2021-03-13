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
    Satellite.objects.filter(name=satellite_name).update(
        distance_from_transmitter=distance,
        message_received=json.dumps(message),
    )


def update_satellites_bulk(satellites):
    """
    Update the distances from the transmitter to every satellite, 
    and the message received by all of them.

    Args:
        - satellites (list(dict)): List of dicts that represent the information about each satellite.
    """
    satellites_to_update = []
    for satellite in satellites:
        satellite_to_update = Satellite.objects.get(name=satellite['name'])
        satellite_to_update.distance_from_transmitter = satellite['distance']
        satellite_to_update.message_received = json.dumps(satellite['message'])

        satellites_to_update.append(satellite_to_update)

    Satellite.objects.bulk_update(
        satellites_to_update,
        ['distance_from_transmitter', 'message_received'],
    )
    

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
