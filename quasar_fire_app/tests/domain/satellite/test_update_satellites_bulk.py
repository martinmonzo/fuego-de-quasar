import json

from django.test import TestCase

from quasar_fire_app.domain.satellite import update_satellites_bulk
from quasar_fire_app.models.satellite import Satellite


class TestCaseUpdateSatellitesBulk(TestCase):

    def setUp(self):
        self.satellites = [
            {
                'name': 'kenobi',
                'distance': 100,
                'message': ['Hello', '', '', 'you?']
            },
            {
                'name': 'skywalker',
                'distance': 200,
                'message': ['', 'how', '', '']
            },
            {
                'name': 'sato',
                'distance': 300,
                'message': ['Hello', '', 'are', '']
            }
        ]
    
    def test_satellite_should_be_updated_and_saved_to_the_db(self):
        """Test that each instance of Satellite updated by update_satellites_bulk is updated in the DB."""        
        update_satellites_bulk(self.satellites)

        for satellite in self.satellites:
            satellite_from_db = Satellite.objects.get(name=satellite['name'])

            assert satellite_from_db.distance_from_transmitter == satellite['distance']
            assert satellite_from_db.message_received == json.dumps(satellite['message'])
