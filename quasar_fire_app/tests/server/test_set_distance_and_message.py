import json
from mock import patch

from django.test import TestCase

from rest_framework.exceptions import APIException
from rest_framework.test import APIRequestFactory

from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessage


class TestCaseSetDistanceAndMessage(TestCase):

    post_url = '/topsecret_split/{}'
    
    def setUp(self):
        self.factory = APIRequestFactory()

    def post(self, data, satellite_name=''):
        request = self.factory.post(
            self.post_url.format(satellite_name),
            data,
            format='json',
        )
        request.data = json.loads(request.body)
        return request, satellite_name 

    def test_should_raise_api_exception_if_kwargs_do_not_have_satellite_name(self):
        """
        Test that SetDistanceAndMessage(request) raises 
        APIException because no kwargs['satellite_name'] is sent. 
        """
        request, satellite_name = self.post({'fake-key': []})

        with self.assertRaises(APIException):
            SetDistanceAndMessage(request)
    
    def test_should_raise_api_exception_if_request_do_not_have_distance(self):
        """
        Test that SetDistanceAndMessage(request, satellite_name='kenobi')
        raises APIException because no distance is sent in the request. 
        """
        request, satellite_name = self.post(
            {'message': ['Hello', '', '', 'you?']},
            'kenobi',
        )

        with self.assertRaises(APIException):
            SetDistanceAndMessage(request, satellite_name=satellite_name)

    def test_should_raise_api_exception_if_request_do_not_have_message(self):
        """
        Test that SetDistanceAndMessage(request, satellite_name='kenobi')
        raises APIException because no distance is sent in the request. 
        """
        request, satellite_name = self.post(
            {'distance': 100.5},
            'kenobi',
        )

        with self.assertRaises(APIException):
            SetDistanceAndMessage(request, satellite_name=satellite_name)

    @patch('quasar_fire_app.server.set_distance_and_message.update_satellite')
    def test_should_call_update_satellite_if_data_is_valid(self, patch_update_satellite):
        """
        Test that SetDistanceAndMessage(request, satellite_name='kenobi')
        works successfully, that is, that update_satellite will be called.
        """
        distance = 100.5
        message = ['Hello', '', '', 'you?']

        request, satellite_name = self.post(
            {
                'distance': distance,
                'message': message,
            },
            'kenobi',
        )

        SetDistanceAndMessage(request, satellite_name=satellite_name)

        patch_update_satellite.assert_called_once_with(satellite_name, distance, message)
