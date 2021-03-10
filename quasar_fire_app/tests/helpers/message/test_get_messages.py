from quasar_fire_app.helpers.message import get_messages
from quasar_fire_app.models.satellite import Satellite
from quasar_fire_app.tests.helpers.message.base import BaseTestCaseMessage


class TestCaseGetMessages(BaseTestCaseMessage):

    def test_should_message_received_by_satellites(self):
        """
        Test that get_distances returns a dict with name and distance_from_transmitter, 
        with distance_from_transmitter = None for every item, because no distance is known yet.
        """
        self.update_all_messages()
        satellites_info = Satellite.objects.all()

        result = get_messages(satellites_info)
        
        assert result == [
            ["Hello", "", "", "you?"],
            ["Hello", "", "", "you?"],
            ["Hello", "", "", "you?"],
        ]
