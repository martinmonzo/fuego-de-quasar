
import json

from django.test import TestCase

from quasar_fire_app.domain.satellite import update_satellite
from quasar_fire_app.models.satellite import Satellite

class TestCaseSatelliteModel(TestCase):

    def setUp(self):
        self.satellite = Satellite.objects.create(
            name='fake-name',
            x_position=100,
            y_position=200,
        )

    def test_satellite_creation_should_have_correct_values(self):
        """Test that the attributes of a Satellite instance are set properly after creation."""

        assert self.satellite.name == 'fake-name'
        assert self.satellite.x_position == 100
        assert self.satellite.y_position == 200
        assert self.satellite.distance_from_transmitter is None
        assert self.satellite.message_received is None
    
    def test_satellite_update_should_save_correct_values(self):
        """Test that the attributes of a Satellite instance are updated properly."""
        new_distance = 50.5
        new_message = ['Hello', '', '', 'you?']

        update_satellite('fake-name', new_distance, new_message)

        satellite_from_db = Satellite.objects.get(name=self.satellite.name)

        assert satellite_from_db.name == self.satellite.name
        assert satellite_from_db.x_position == 100
        assert satellite_from_db.y_position == 200
        assert satellite_from_db.distance_from_transmitter == new_distance
        assert satellite_from_db.message_received == json.dumps(new_message)
