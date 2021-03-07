import json

from quasar_fire_app.models.satellite import Satellite


def update_satellite(satellite_name: str, distance: float, message: str) -> None:
    satellite = Satellite.objects.get(name=satellite_name)

    satellite.distance_from_transmitter = distance
    satellite.message_received = json.dumps(message)
    satellite.save()
