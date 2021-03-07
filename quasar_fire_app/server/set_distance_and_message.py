from quasar_fire_app.domain.satellite import update_satellite
from quasar_fire_app.server.base import BaseAction


class SetDistanceAndMessageAction(BaseAction):

    def __init__(self, request, **kwargs):
        super().__init__(request, **kwargs)

    def validate(self, **kwargs):
        self.satellite_name = kwargs['satellite_name']
        self.distance = self.request.data['distance']
        self.message = self.request.data['message']

    def run(self):
        update_satellite(
            self.satellite_name,
            self.distance,
            self.message,
        )
