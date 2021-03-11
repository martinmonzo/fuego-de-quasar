from rest_framework.exceptions import APIException

from quasar_fire_app.domain.location import get_transmitter_location
from quasar_fire_app.domain.message import get_original_message
from quasar_fire_app.domain.satellite import get_all_satellites_info
from quasar_fire_app.helpers.distance import (
    get_distances,
    is_there_any_unknown_distance,
)
from quasar_fire_app.helpers.message import (
    get_messages,
    is_there_any_unknown_message,
)
from quasar_fire_app.server.base import BaseAction


class GetLocationAndMessage(BaseAction):

    def validate(self):
        # Retrieve from the DB the information about the satellites.
        satellites_info = get_all_satellites_info()
        
        # If some distance or some message could not be discovered, there is no
        # enough information to discover the location of the transmitter
        if is_there_any_unknown_distance(satellites_info):
            raise APIException('The distance to at least one satellite could not be determined.')
        if is_there_any_unknown_message(satellites_info):
            raise APIException('At least one satellite did not receive any message.')

        # Get the distances from the transmitter to every satellite.
        distances_by_satellite = get_distances(satellites_info)
        self.distances = [
            distances_by_satellite['kenobi'],
            distances_by_satellite['skywalker'],
            distances_by_satellite['sato'],
        ]        
        # Get messages received. In this case, we don't care about which
        # satellite received which message. We only take care about the messages.
        self.messages = get_messages(satellites_info)

    def run(self):
        location = get_transmitter_location(self.distances)
        message = get_original_message(self.messages)

        self.response = {
            'position': {
                'x': location[0],
                'y': location[1],
            },
            'message': message,
        }
