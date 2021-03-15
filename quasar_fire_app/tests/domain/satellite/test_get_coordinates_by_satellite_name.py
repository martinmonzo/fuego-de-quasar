from django.test import TestCase

from quasar_fire_app.domain.satellite import get_coordinates_by_satellite_name
from quasar_fire_app.models.satellite import Satellite


class TestCaseUpdateSatellite(TestCase):

    def test_should_retrieve_right_x_and_y_positions(self):
        """
        Test that get_coordinates_by_satellite_name retrieves
        the (X,Y) coordinates of each satellite.
        """
        satellites = Satellite.objects.all()
        
        result = get_coordinates_by_satellite_name()

        assert result == {
            satellite.name: {
                'x_position': satellite.x_position,
                'y_position': satellite.y_position,
            }
            for satellite in satellites
        }
