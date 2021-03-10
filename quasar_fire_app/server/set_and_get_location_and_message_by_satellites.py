from quasar_fire_app.domain.satellite import update_satellites_bulk
from quasar_fire_app.helpers.distance import get_distance_by_satellite
from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage


class SetAndGetLocationAndMessageBySatellites(GetLocationAndMessage):

    def validate(self):
        satellites = self.request.data['satellites']
        
        # Get the distance from the transmitter to each satellite.
        distance_from_kenobi = get_distance_by_satellite(satellites, 'kenobi')
        distance_from_skywalker = get_distance_by_satellite(satellites, 'skywalker')
        distance_from_sato = get_distance_by_satellite(satellites, 'sato')
        
        self.distances = [distance_from_kenobi, distance_from_skywalker, distance_from_sato]

        # Get messages received. In this case, we don't care about which
        # satellite received which message. We only take care about the messages.
        self.messages = [satellite['message'] for satellite in satellites]
        
        # Save the distances and messages in the DB
        update_satellites_bulk(satellites)
