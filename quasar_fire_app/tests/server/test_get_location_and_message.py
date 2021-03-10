from mock import patch

from django.test import TestCase
from rest_framework.exceptions import APIException
from rest_framework.test import APIRequestFactory

from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage


class TestCaseGetLocationAndMessage(TestCase):

    post_url = '/topsecret_split/{}'
    
    def setUp(self):
        self.factory = APIRequestFactory()

    def get(self):
        return self.factory.get(self.post_url.format('kenobi'))
    
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_all_satellites_info',
        side_effect=Exception(),
    )
    def test_should_raise_api_exception_if_get_all_satellites_info_fails(
        self,
        patch_get_all_satellites_info,
    ):
        """
        Test that GetLocationAndMessage(request) raises APIException 
        when get_all_satellites_info fails. 
        """
        request = self.get()

        with self.assertRaises(APIException):
            GetLocationAndMessage(request)
    
    @patch(
        'quasar_fire_app.server.get_location_and_message.is_there_any_unknown_distance',
        return_value=True,
    )
    def test_should_raise_api_exception_if_there_are_unknown_distances(
        self,
        patch_is_there_any_unknown_distance,
    ):
        """
        Test that GetLocationAndMessage(request) raises APIException 
        if is_there_any_unknown_distance returns True. 
        """
        request = self.get()

        with self.assertRaises(APIException):
            GetLocationAndMessage(request)

    @patch(
        'quasar_fire_app.server.get_location_and_message.is_there_any_unknown_message',
        side_effect=True,
    )
    def test_should_raise_api_exception_if_there_are_unknown_messages(
        self,
        patch_is_there_any_unknown_message,
    ):
        """
        Test that GetLocationAndMessage(request) raises APIException 
        if is_there_any_unknown_message returns True.
        """
        request = self.get()

        with self.assertRaises(APIException):
            GetLocationAndMessage(request)

    @patch('quasar_fire_app.server.get_location_and_message.get_all_satellites_info')
    @patch(
        'quasar_fire_app.server.get_location_and_message.is_there_any_unknown_distance',
        return_value=False,
    )
    @patch(
        'quasar_fire_app.server.get_location_and_message.is_there_any_unknown_message',
        return_value=False,
    )
    @patch('quasar_fire_app.server.get_location_and_message.get_distances')
    @patch('quasar_fire_app.server.get_location_and_message.get_messages')
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_transmitter_location',
        return_value=(100.0, 200.0),
    )
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_original_message',
        return_value='This is the original message',
    )
    def test_should_retrieve_response(
        self,
        patch_get_original_message,
        patch_get_transmitter_location,
        patch_get_messages,
        patch_get_distances,
        patch_is_there_any_unknown_message,
        patch_is_there_any_unknown_distance,
        patch_get_all_satellites_info,
    ):
        """Test that SetAndGetLocationAndMessageBySatellites(request) works successfully."""
        request = self.get()

        response = GetLocationAndMessage(request).response

        assert response['position'] == {
            'x': 100.0,
            'y': 200.0,
        }
        assert response['message'] == 'This is the original message'
