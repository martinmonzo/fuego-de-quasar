import json
from mock import patch
from parameterized import parameterized

from django.test import TestCase

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.test import APIClient

from quasar_fire_app.models.satellite import Satellite
from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage
from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessage


class BaseTestCaseTopSecretSplit(TestCase):

    url = '/topsecret_split/{}/'

    def setUp(self):
        self.client = APIClient()

class TestCaseTopSecretSplitPost(BaseTestCaseTopSecretSplit):
    
    def post(self, data, satellite_name=''):
        return self.client.post(
            self.url.format(satellite_name),
            data,
            format='json',
        )

    @parameterized.expand([
        ([{"message": ["Hello", "", "", "you?"]}]),  # Data without distance
        ([{"distance": 50}]),  # Data without message
    ])
    def test_should_return_404_for_invalid_payload(self, payload):
        """Test that the view returns a response code 404 when the payload is invalid."""
        response = self.post(payload, 'kenobi')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch.object(SetDistanceAndMessage, 'validate', side_effect=APIException())
    def test_should_return_404_response_raises_api_exception(self, patch_validate):
        """
        Test that the view returns a response code 404 
        when the call to the server action raises an APIException.
        """
        data = {
            "message": ["Hello", "", "", "you?"],
            "distance": 50,
        }

        response = self.post(data, 'kenobi')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_should_pass_successfully_for_correct_payload(self):
        """Test that the view returns a response code 200 when the payload is valid."""
        data = {
            "message": ["Hello", "", "", "you?"],
            "distance": 50,
        }

        response = self.post(data, 'kenobi')

        assert response.status_code == status.HTTP_200_OK


class TestCaseTopSecretSplitGet(BaseTestCaseTopSecretSplit):

    def get(self, satellite_name=''):
        return self.client.get(
            self.url.format(satellite_name),
            format='json',
        )

    def update_satellite_by_name(self, satellite_name, distance, message):
        satellite = Satellite.objects.get(name=satellite_name)
        satellite.distance_from_transmitter = distance
        satellite.message_received = json.dumps(message)
        satellite.save()

    @patch.object(GetLocationAndMessage, 'validate', side_effect=APIException())
    def test_should_return_404_response_raises_api_exception(self, patch_validate):
        """
        Test that the view returns a response code 404 
        when the call to the server action raises an APIException.
        """
        response = self.get('kenobi')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'There is no enough information.'

    def test_should_pass_successfully_when_there_is_enough_information(self):
        """
        Test that the view returns a response code 200 and the expected 
        data when the information in the DB is right and complete.
        """
        self.update_satellite_by_name('kenobi', 670.8203932, ["Hello", "", "are", ""])
        self.update_satellite_by_name('skywalker', 200, ["", "", "are", "you?"])
        self.update_satellite_by_name('sato', 400, ["Hello", "how", "", ""])

        response = self.get('kenobi')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Hello how are you?'
        assert response.data['position'] == {'x': 100.0, 'y': 100.0}
