import json

from quasar_fire_app.models.satellite import Satellite


def update_satellite(satellite_name: str, distance: float, message: str) -> None:
    """
    Update the distance from a satellite to the transmitter, 
    and the message received by it, given a satellite name.

    Args:
        - satellite_name: name of the satellite to filter by.
        - distance: distance from the satellite to the transmitter.
        - message: List of string that represents the message received in the satellite.
    """
    satellite = Satellite.objects.get(name=satellite_name)

    satellite.distance_from_transmitter = distance
    satellite.message_received = json.dumps(message)
    satellite.save()
