from mock import patch
from parameterized import parameterized

from django.test import TestCase

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.test import APIClient

from quasar_fire_app.server.set_distance_and_message import SetDistanceAndMessageAction


class TestCaseTopSecretSplitPost(TestCase):

    post_url = '/topsecret_split/{}/'
    
    def setUp(self):
        self.client = APIClient()

    def post(self, data, satellite_name=''):
        return self.client.post(
            self.post_url.format(satellite_name),
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

    @patch.object(SetDistanceAndMessageAction, 'validate', side_effect=APIException())
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
