
from django.test import TestCase

from quasar_fire_app.models.satellite import Satellite

class TestCaseSatelliteModel(TestCase):

    def test_satellite_creation_should_have_correct_values(self):
        """Test that the attributes of a Satellite instance are set properly after creation."""
        
        satellite = Satellite(
            name="fake-name",
            x_position=100,
            y_position=200,
        )

        assert satellite.name == "fake-name"
        assert satellite.x_position == 100
        assert satellite.y_position == 200
        assert satellite.distance_from_transmitter is None
