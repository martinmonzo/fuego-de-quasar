from parameterized import parameterized

from django.test import TestCase

from quasar_fire_app.domain.satellite import get_coordinates_by_satellite_name
from quasar_fire_app.models.satellite import Satellite


class TestCaseUpdateSatellite(TestCase):

    @parameterized.expand([
        ('kenobi',),
        ('skywalker',),
        ('sato',),
    ])
    def test_should_retrieve_x_and_y_positions(self, satellite_name):
        """
        Test that get_coordinates_by_satellite_name retrieves
        the (X,Y) coordinates of the desired satellite.
        """
        satellite = Satellite.objects.get(name=satellite_name)
        
        result = get_coordinates_by_satellite_name(satellite_name)

        assert result == (satellite.x_position, satellite.y_position)
