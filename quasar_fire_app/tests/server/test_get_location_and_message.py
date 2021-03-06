import json
from mock import patch
from parameterized import parameterized

from django.test import TestCase
from django.test.client import (
    encode_multipart,
    RequestFactory,
)
from rest_framework.test import APIRequestFactory



from rest_framework import status
from rest_framework.exceptions import APIException


from quasar_fire_app.server.get_location_and_message import GetLocationAndMessageAction


class TestCaseGetLocationAndMessageAction(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.post_url = '/topsecret/'

    def post(self, data={'satellites': []}):
        request = self.factory.post(
            self.post_url,
            data,
            format='json',
        )
        request.data = json.loads(request.body)
        return request

    def test_should_raise_api_exception_if_request_does_not_have_satellites(self):
        """
        Test that GetLocationAndMessageAction(request) raises APIException 
        when the request data does not have the key 'satellites'. 
        """
        request = self.post({'fake-key': []})

        with self.assertRaises(APIException):
            GetLocationAndMessageAction(request)
    
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_distance_by_satellite',
        side_effect=KeyError(),
    )
    def test_should_raise_api_exception_if_get_distance_by_satellite_fails(
        self,
        patch_get_distance_by_satellite,
    ):
        """
        Test that GetLocationAndMessageAction(request) raises APIException 
        when get_distance_by_satellite fails. 
        """
        request = self.post()

        with self.assertRaises(APIException):
            GetLocationAndMessageAction(request)
    
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_location',
        side_effect=Exception(),
    )
    def test_should_raise_api_exception_if_get_location_fails(
        self,
        patch_get_location,
    ):
        """
        Test that GetLocationAndMessageAction(request) raises APIException 
        when get_location fails. 
        """
        request = self.post()

        with self.assertRaises(APIException):
            GetLocationAndMessageAction(request)

    @patch(
        'quasar_fire_app.server.get_location_and_message.get_message',
        side_effect=Exception(),
    )
    def test_should_raise_api_exception_if_get_message_fails(
        self,
        patch_get_message,
    ):
        """
        Test that GetLocationAndMessageAction(request) raises APIException 
        when get_message fails. 
        """
        request = self.post()

        with self.assertRaises(APIException):
            GetLocationAndMessageAction(request)

    @patch(
        'quasar_fire_app.server.get_location_and_message.get_distance_by_satellite',
        return_value=10,
    )
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_location',
        return_value=(100.0, 200.0),
    )
    @patch(
        'quasar_fire_app.server.get_location_and_message.get_message',
        return_value='This is the original message',
    )
    def test_should_retrieve_response_if_get_location_and_get_message_works_successfully(
        self,
        patch_get_message,
        patch_get_location,
        patch_get_distance_by_satellite,
    ):
        """Test that GetLocationAndMessageAction(request) works successfully."""
        request = self.post()

        response = GetLocationAndMessageAction(request).response

        assert response['position'] == {
            'x': 100.0,
            'y': 200.0,
        }
        assert response['message'] == 'This is the original message'
