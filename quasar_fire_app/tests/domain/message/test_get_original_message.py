from django.test import TestCase

from quasar_fire_app.domain.message import get_original_message


class TestCaseGetOriginalMessage(TestCase):

    def test_should_raise_exception_for_messages_of_different_length(self):
        """
        Test that get_original_message returns False when the messages 
        received by each satellite have different lengths.
        """
        first_message = ['Hello', 'how', '', '']
        second_message = ['', '', 'are', 'you?']
        third_message = ['Hello', '']
        messages = [first_message, second_message, third_message]

        with self.assertRaises(Exception) as error:
            get_original_message(messages)
        
        assert error.exception.args[0] == 'The messages received by the satellites does not have the same length.'
    
    def test_should_raise_exception_for_missing_word_in_all_messages(self):
        """
        Test that get_original_message returns False when every
        message has a blank word ("") in the same position.
        """
        first_message = ['', 'how', '', '']
        second_message = ['', '', 'are', '']
        third_message = ['', '', '', 'you?']
        messages = [first_message, second_message, third_message]

        with self.assertRaises(Exception) as error:
            get_original_message(messages)

        assert error.exception.args[0] == 'The word at this position could not be received by any satellite.'
    
    def test_should_raise_exception_for_messages_with_different_word_in_same_position(self):
        """
        Test that get_original_message returns False when some of the
        messages have 2 different words in the same position.
        """
        first_message = ['Hello', 'how', '', '']
        second_message = ['Hi', '', 'are', '']
        third_message = ['', '', '', 'you?']
        messages = [first_message, second_message, third_message]

        with self.assertRaises(Exception) as error:
            get_original_message(messages)

        assert error.exception.args[0] == 'Different words were received by the satellites at this position.'
    
    def test_should_return_original_message(self):
        """
        Test that get_original_message returns the original message when
        every word was received properly in at least one satellite.
        """
        first_message = ['Hello', '', '', 'you?']
        second_message = ['', 'how', 'are', '']
        third_message = ['', 'how', '', 'you?']
        messages = [first_message, second_message, third_message]

        result = get_original_message(messages)

        assert result == 'Hello how are you?'
