import json
from mock import patch

from django.test import TestCase
from rest_framework.exceptions import APIException
from rest_framework.test import APIRequestFactory

from quasar_fire_app.server.get_location_and_message_by_satellites import GetLocationAndMessage


class TestCaseGetLocationAndMessage(TestCase):

    post_url = '/topsecret_split/{}'
    
    def setUp(self):
        self.factory = APIRequestFactory()

    def post(self, data={'satellites': []}):
        request = self.factory.post(
            self.post_url,
            data,
            format='json',
        )
        request.data = json.loads(request.body)
        return request
    
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
        request = self.post()

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
        request = self.post()

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
        request = self.post()

        with self.assertRaises(APIException):
            GetLocationAndMessage(request)
