from quasar_fire_app.domain.location import (
    get_distance_by_satellite,
    get_location,
)
from quasar_fire_app.domain.message import get_message
from quasar_fire_app.server.base import BaseAction


class GetLocationAndMessageAction(BaseAction):

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

    def run(self):
        location = get_location(self.distances)
        message = get_message(self.messages)

        self.response = {
            'position': {
                'x': location[0],
                'y': location[1],
            },
            'message': message,
        }
