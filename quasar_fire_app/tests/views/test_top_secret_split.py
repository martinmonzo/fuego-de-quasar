import json
from mock import patch
from parameterized import parameterized

from rest_framework import status
from rest_framework.exceptions import APIException

from quasar_fire_app.common.errors import GENERIC_ERROR_NO_INFORMATION_AVAILABLE
from quasar_fire_app.models.satellite import Satellite
from quasar_fire_app.server.get_location_and_message import GetLocationAndMessage
from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessage
from quasar_fire_app.tests.views.base import BaseTestCaseAPIView


class TestCaseTopSecretSplitPost(BaseTestCaseAPIView):

    url = '/topsecret_split/{}/'
    
    def post(self, data, satellite_name):
        return self.client.post(
            self.url.format(satellite_name),
            data,
            format='json',
        )

    @parameterized.expand([
        ([{'message': ['Hello', '', '', 'you?']}]),  # Data without distance
        ([{'distance': 50}]),  # Data without message
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
            'message': ['Hello', '', '', 'you?'],
            'distance': 50,
        }

        response = self.post(data, 'kenobi')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_should_pass_successfully_for_correct_payload(self):
        """Test that the view returns a response code 200 when the payload is valid."""
        data = {
            'message': ['Hello', '', '', 'you?'],
            'distance': 50,
        }

        response = self.post(data, 'kenobi')

        assert response.status_code == status.HTTP_200_OK


class TestCaseTopSecretSplitGet(BaseTestCaseAPIView):

    url = '/topsecret_split/'

    def get(self):
        return self.client.get(
            self.url,
            format='json',
        )

    def update_satellites_bulk(self, satellites):
        satellites_to_update = []
        for satellite in satellites:
            satellite_to_update = Satellite.objects.get(name=satellite['name'])
            satellite_to_update.distance_from_transmitter = satellite['distance']
            satellite_to_update.message_received = json.dumps(satellite['message'])

            satellites_to_update.append(satellite_to_update)

        Satellite.objects.bulk_update(
            satellites_to_update,
            ['distance_from_transmitter', 'message_received'],
        )

    @patch.object(GetLocationAndMessage, 'validate', side_effect=APIException())
    def test_should_return_404_response_raises_api_exception(self, patch_validate):
        """
        Test that the view returns a response code 404 
        when the call to the server action raises an APIException.
        """
        response = self.get()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == GENERIC_ERROR_NO_INFORMATION_AVAILABLE

    def test_should_pass_successfully_when_there_is_enough_information(self):
        """
        Test that the view returns a response code 200 and the expected 
        data when the information in the DB is right and complete.
        """
        satellites = [
            {'name': 'kenobi', 'distance': 670.8203932, 'message': ['Hello', '', 'are', '']},
            {'name': 'skywalker', 'distance': 200, 'message': ['', '', 'are', 'you?']},
            {'name': 'sato', 'distance': 400, 'message': ['Hello', 'how', '', '']},
        ]
        self.update_satellites_bulk(satellites)

        response = self.get()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Hello how are you?'
        assert response.data['position'] == {'x': 100.0, 'y': 100.0}
