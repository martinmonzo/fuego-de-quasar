import json

from django.test import TestCase

from quasar_fire_app.domain.satellite import update_satellite
from quasar_fire_app.models.satellite import Satellite


class TestCaseUpdateSatellite(TestCase):

    def test_satellite_should_be_updated_and_saved_to_the_db(self):
        """Test that the instance of Satellite updated by update_satellite is updated in the DB."""        
        satellite_name = 'kenobi'
        new_distance = 100.5
        new_message = ['Hello', '', '', 'you?']
        
        satellite = Satellite.objects.get(name=satellite_name)
        assert satellite.distance_from_transmitter is None
        assert satellite.message_received is None

        update_satellite(satellite_name, new_distance, new_message)

        satellite = Satellite.objects.get(name=satellite_name)
        assert satellite.distance_from_transmitter == new_distance
        assert satellite.message_received == json.dumps(new_message)
