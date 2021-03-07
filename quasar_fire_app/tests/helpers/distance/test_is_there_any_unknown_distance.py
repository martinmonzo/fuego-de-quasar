from django.test import TestCase

from quasar_fire_app.helpers.distance import is_there_any_unknown_distance
from quasar_fire_app.models.satellite import Satellite


class TestCaseIsThereAnyUnknownDistance(TestCase):

    def update_all_distances(self):
        kenobi = Satellite.objects.get(name='kenobi')
        skywalker = Satellite.objects.get(name='skywalker')
        sato = Satellite.objects.get(name='sato')

        new_distance = 100.0
        
        kenobi.distance_from_transmitter = new_distance
        skywalker.distance_from_transmitter = new_distance
        sato.distance_from_transmitter = new_distance

        Satellite.objects.bulk_update([kenobi, skywalker, sato], ['distance_from_transmitter'])

    def test_should_return_true_if_some_distances_are_unknown(self):
        """
        Test that is_there_any_unknown_distance returns True when 
        the distance from the transmitter to some satellites is unknown.
        """
        satellites_info = Satellite.objects.all()

        result = is_there_any_unknown_distance(satellites_info)

        assert result is True
    
    def test_should_return_false_if_every_distance_is_known(self):
        """
        Test that is_there_any_unknown_distance returns False when 
        the distance from the transmitter to every satellite is known.
        """
        self.update_all_distances()
        satellites_info = Satellite.objects.all()

        result = is_there_any_unknown_distance(satellites_info)

        assert result is False
