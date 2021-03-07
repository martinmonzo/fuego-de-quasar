from mock import patch
from parameterized import parameterized

from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.test import APIClient

from quasar_fire_app.server.get_location_and_message_by_satellites import GetLocationAndMessageBySatellites


class TestCaseTopSecretPost(TestCase):
    
    post_url = '/topsecret/'

    def setUp(self):
        self.client = APIClient()

    def post(self, data):
        return self.client.post(
            self.post_url,
            {
                "satellites": data,
            },
            format='json',
        )

    def get_valid_satellites(self):
        return [
            {
                "name": "sato",
                "distance": 282.84271259,
                "message": ["Hello", "", "are", ""]
            },
            {
                "name": "kenobi",
                "distance": 943.3981132,
                "message": ["", "how", "are", ""]
            },
            {
                "name": "skywalker",
                "distance": 447.21359559,
                "message": ["", "how", "", "you?"]
            },
        ]

    @parameterized.expand([
        # Payload has less than 3 satellites
        ([[
            {"name": "fake-name", "distance": 50, "message": ["Hello", "how", "are", "you?"]},
        ]]),
        # Payload has more than 3 satellites
        ([[
            {"name": "fake-name-1", "distance": 50, "message": ["Hello", "", "", "you?"]},
            {"name": "fake-name-2", "distance": 100, "message": ["", "how", "", "you?"]},
            {"name": "fake-name-3", "distance": 200, "message": ["Hello", "", "are", ""]},
            {"name": "fake-name-4", "distance": 500, "message": ["Hello", "how", "", ""]},
        ]]),
        # Satellites without name
        ([[
            {"distance": 50, "message": ["Hello", "", "", "you?"]},
            {"distance": 100, "message": ["", "how", "", "you?"]},
            {"distance": 200, "message": ["Hello", "", "are", ""]},
        ]]),
        # Satellites without distance
        ([[
            {"name": 'fake-name-1', "message": ["Hello", "", "", "you?"]},
            {"name": 'fake-name-2', "message": ["", "how", "", "you?"]},
            {"name": 'fake-name-3', "message": ["Hello", "", "are", ""]},
        ]]),
        # Satellites without message
        ([[
            {"name": 'fake-name-1', "distance": 50},
            {"name": 'fake-name-2', "distance": 100},
            {"name": 'fake-name-3', "distance": 200},
        ]]),
        # names are not string
        ([[
            {"name": 1, "distance": 50, "message": ["Hello", "", "", "you?"]},
            {"name": [], "distance": 100, "message": ["", "how", "", ""]},
            {"name": None, "distance": 200, "message": ["Hello", "", "are", ""]},
        ]]),
        # # distances are not positive numbers
        ([[
            {"name": "fake-name-1", "distance": -50, "message": ["Hello", "", "", "you?"]},
            {"name": "fake-name-2", "distance": "Hello", "message": ["", "how", "", ""]},
            {"name": "fake-name-3", "distance": [], "message": ["Hello", "", "are", ""]},
        ]]),
        # # messages are not lists of string
        ([[
            {"name": "fake-name-1", "distance": 50, "message": [50, None, []]},
            {"name": "fake-name-2", "distance": 100, "message": 5},
            {"name": "fake-name-3", "distance": 200, "message": "Hello"},
        ]]),
    ])
    def test_should_return_404_for_invalid_payload(self, satellites):
        """Test that the view returns a response code 404 when the payload is invalid."""
        response = self.post(satellites)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch.object(GetLocationAndMessageBySatellites, 'validate', side_effect=APIException())
    def test_should_return_404_response_raises_api_exception(self, patch_validate):
        """
        Test that the view returns a response code 404 
        when the call to the server action raises an APIException.
        """
        satellites = self.get_valid_satellites()

        response = self.post(satellites)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_should_pass_successfully_for_correct_payload(self):
        """
        Test that the view returns a response code 200 
        and the expected data when the payload is valid.
        """
        satellites = self.get_valid_satellites()

        response = self.post(data=satellites)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Hello how are you?'
        assert response.data['position'] == {'x': 300.0, 'y': 300.0}
