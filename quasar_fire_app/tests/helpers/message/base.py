from django.test import TestCase

from quasar_fire_app.models.satellite import Satellite


class BaseTestCaseMessage(TestCase):

    def update_all_messages(self):
        kenobi = Satellite.objects.get(name='kenobi')
        skywalker = Satellite.objects.get(name='skywalker')
        sato = Satellite.objects.get(name='sato')

        new_message = '["Hello", "", "", "you?"]'
        
        kenobi.message_received = new_message
        skywalker.message_received = new_message
        sato.message_received = new_message

        Satellite.objects.bulk_update([kenobi, skywalker, sato], ['message_received'])
