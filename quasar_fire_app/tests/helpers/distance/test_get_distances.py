from django.test import TestCase

from quasar_fire_app.helpers.distance import get_distances
from quasar_fire_app.models.satellite import Satellite


class TestCaseGetDistances(TestCase):

    def update_distance_by_satellite(self, satellite_name):
        Satellite.objects.filter(name=satellite_name).update(
            distance_from_transmitter=100.0,
        )

    def test_should_return_none_distances_if_no_distance_is_known(self):
        """
        Test that get_distances returns a dict with name and distance_from_transmitter, 
        with distance_from_transmitter = None for every item, because no distance is known yet.
        """
        satellites_info = Satellite.objects.all()

        result = get_distances(satellites_info)
        
        assert result == {'kenobi': None, 'skywalker': None, 'sato': None}
        
    def test_should_return_distances_for_known_distances(self):
        """
        Test that get_distances returns a dict with name and distance_from_transmitter, 
        with distance_from_transmitter = None for every item, because no distance is known yet.
        """
        self.update_distance_by_satellite('kenobi')
        satellites_info = Satellite.objects.all()

        result = get_distances(satellites_info)
        
        assert result == {'kenobi': 100.0, 'skywalker': None, 'sato': None}
        