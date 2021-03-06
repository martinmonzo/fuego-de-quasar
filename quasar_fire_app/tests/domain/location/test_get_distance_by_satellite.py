from django.test import TestCase

from quasar_fire_app.domain.location import get_distance_by_satellite


class TestCaseGetDistanceBySatellite(TestCase):

    def setUp(self):
        self.satellites = [
            {
                'name': 'first',
                'distance': 100.5,
                'message': ["Hello,", "", "", "a", ""],
            },
            {
                'name': 'second',
                'distance': 200,
                'message': ["", "", "is", "", "message"],
            },
            {
                'name': 'third',
                'distance': 50,
                'message': ["Hello,", "this", "", "", "message"],
            },
        ]

    def test_should_raise_key_error_if_the_satellite_name_passed_does_not_exist_in_satellites(self):
        """
        Test that get_distance_by_satellite raises KeyError if the name of 
        the desired satellite does not exist in the list of satellites received.
        """
        with self.assertRaises(KeyError):
            get_distance_by_satellite(self.satellites, 'fake-satellite-name')
    
    def test_should_return_the_distance_to_the_desired_satellite(self):
        """
        Test that get_distance_by_satellite returns the distance from the transmitter
        to the satellite whose name matches with the argument sent.
        """
        result = get_distance_by_satellite(self.satellites, 'third')

        assert result == 50
