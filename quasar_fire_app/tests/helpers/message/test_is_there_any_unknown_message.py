from django.test import TestCase

from quasar_fire_app.helpers.message import is_there_any_unknown_message
from quasar_fire_app.models.satellite import Satellite


class TestCaseIsThereAnyUnknownMessage(TestCase):

    def update_all_messages(self):
        kenobi = Satellite.objects.get(name='kenobi')
        skywalker = Satellite.objects.get(name='skywalker')
        sato = Satellite.objects.get(name='sato')

        new_message = ["Hello", "", "", "you?"]
        
        kenobi.message_received = new_message
        skywalker.message_received = new_message
        sato.message_received = new_message

        Satellite.objects.bulk_update([kenobi, skywalker, sato], ['message_received'])

    def test_should_return_true_if_some_messages_are_unknown(self):
        """
        Test that is_there_any_unknown_message returns True
        when some satellites have not received any message.
        """
        satellites_info = Satellite.objects.all()

        result = is_there_any_unknown_message(satellites_info)

        assert result is True
    
    def test_should_return_false_if_every_satellite_received_a_message(self):
        """
        Test that is_there_any_unknown_message returns False 
        when every satellite has received a message.
        """
        self.update_all_messages()
        satellites_info = Satellite.objects.all()

        result = is_there_any_unknown_message(satellites_info)

        assert result is False
