from django.test import TestCase

from quasar_fire_app.helpers.message import get_messages
from quasar_fire_app.models.satellite import Satellite


class TestCaseGetMessages(TestCase):

    def update_all_messages(self):
        kenobi = Satellite.objects.get(name='kenobi')
        skywalker = Satellite.objects.get(name='skywalker')
        sato = Satellite.objects.get(name='sato')

        new_message = '["Hello", "", "", "you?"]'
        
        kenobi.message_received = new_message
        skywalker.message_received = new_message
        sato.message_received = new_message

        Satellite.objects.bulk_update([kenobi, skywalker, sato], ['message_received'])

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
