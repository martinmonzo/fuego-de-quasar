from mock import (
    call,
    patch,
)

from django.test import TestCase

from quasar_fire_app.domain.satellite import update_satellites_bulk


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

    @patch('quasar_fire_app.domain.satellite.update_satellite')
    def test_satellite_should_be_updated_and_saved_to_the_db(self, patch_update_satellite):
        """Test that each instance of Satellite updated by update_satellites_bulk is updated in the DB."""        
        update_satellites_bulk(self.satellites)

        expected_call_args_list = [
            call(satellite['name'], satellite['distance'], satellite['message'])
            for satellite in self.satellites
        ]

        assert patch_update_satellite.call_args_list == expected_call_args_list


