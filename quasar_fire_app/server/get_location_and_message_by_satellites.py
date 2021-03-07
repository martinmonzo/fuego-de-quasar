from quasar_fire_app.domain.location import get_transmitter_location
from quasar_fire_app.domain.message import get_original_message
from quasar_fire_app.helpers.distance import get_distance_by_satellite
from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage


class GetLocationAndMessageBySatellites(GetLocationAndMessage):

    def validate(self):
        satellites = self.request.data['satellites']
        
        # Get distance from the transmitter to each satellite.
        distance_from_kenobi = get_distance_by_satellite(satellites, 'kenobi')
        distance_from_skywalker = get_distance_by_satellite(satellites, 'skywalker')
        distance_from_sato = get_distance_by_satellite(satellites, 'sato')
        
        self.distances = [distance_from_kenobi, distance_from_skywalker, distance_from_sato]

        # Get messages received. In this case, we don't care about which
        # satellite received which message. We only take care about the messages.
        self.messages = [satellite['message'] for satellite in satellites]
