from mock import patch

from django.test import TestCase

from quasar_fire_app.domain.location import get_transmitter_location


class TestCaseGetTransmitterLocation(TestCase):

    def test_should_raise_exception_for_distances_that_dont_match_any_point(self):
        """
        Test that get_transmitter_location returns False when the distances to the
        satellites are not consistent at any point in the plane, that is, 
        the circumferences around each satellite do not share any point in common.
        """
        # If the distance to Kenobi is 10, then the point must be between 
        # -510 and -490 in X-axis and between -210 and -190 in Y-axis.
        distance_to_kenobi = 10
        # If the distance to Skywalker is 0, then the point must be the same as Skywalker 
        # position (X=100, Y=-100), but this is inconsistent with the distance to Kenobi.
        distance_to_skywalker = 0
        # If the distance to Sato is 100, then the point must be 
        # between 400 and 600 in X-axis and between 0 and 200 in Y-axis,
        # but this is inconsistent with the distance to Kenobi and Skywalker.
        distance_to_sato = 100

        with self.assertRaises(Exception) as error:
            get_transmitter_location([distance_to_kenobi, distance_to_skywalker, distance_to_sato])

        assert error.exception.args[0] == 'The retrieved value is not at the specified distances from the satellites.'
    
    @patch('quasar_fire_app.domain.location.is_close', return_value=False)
    def test_should_raise_exception_if_is_close_returns_false_for_some_point(self, patch_is_close):
        """
        Test that get_transmitter_location returns False when the method is_close returns False, which means
        that the compared numbers aren't enough similar or their difference isn't enough little.
        """
        distance_to_kenobi = 100
        distance_to_skywalker = 50
        distance_to_sato = 120

        with self.assertRaises(Exception) as error:
            get_transmitter_location([distance_to_kenobi, distance_to_skywalker, distance_to_sato])

        assert error.exception.args[0] == 'The retrieved value is not at the specified distances from the satellites.'
    
    @patch('quasar_fire_app.domain.location.is_close', return_value=True)
    def test_should_return_some_xy_point_for_distances_that_match_a_point(self, patch_is_close):
        """
        Test that get_transmitter_location returns a point (X,Y) when the distances to the
        satellites are consistent at one point in the plane, that is, 
        the circumferences around each satellite have one point in common.
        """
        # The point (300, 300) is the one in the plane that matches the following distances
        # to Kenobi (-500, -200), Skywalker (100, -100) and Sato (500, 100) respectively
        distance_to_kenobi = 943.3981132
        distance_to_skywalker = 447.2135955
        distance_to_sato = 282.8427125

        expected_point = (300, 300)

        result = get_transmitter_location([distance_to_kenobi, distance_to_skywalker, distance_to_sato])

        assert result == expected_point
