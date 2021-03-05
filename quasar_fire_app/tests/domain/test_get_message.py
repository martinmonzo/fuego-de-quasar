from django.test import TestCase
from quasar_fire_app.domain.get_message import get_message

class TestCaseGetMessage(TestCase):

    def test_should_return_false_for_messages_of_different_length(self):
        """
        Test that get_message returns False when the messages 
        received by each satellite have different lengths.
        """
        
        first_message = ["Hello", "how", "", ""]
        second_message = ["", "", "are", "you?"]
        third_message = ["Hello", ""]
        messages = [first_message, second_message, third_message]

        result = get_message(messages)

        assert result is False
    
    def test_should_return_false_for_missing_word_in_all_messages(self):
        """
        Test that get_message returns False when every
        message has a blank word ("") in the same position.
        """
        
        first_message = ["", "how", "", ""]
        second_message = ["", "", "are", ""]
        third_message = ["", "", "", "you?"]
        messages = [first_message, second_message, third_message]

        result = get_message(messages)

        assert result is False
    
    def test_should_return_false_for_messages_with_different_word_in_same_position(self):
        """
        Test that get_message returns False when some of the
        messages have 2 different words in the same position.
        """
        
        first_message = ["Hello", "how", "", ""]
        second_message = ["Hi", "", "are", ""]
        third_message = ["", "", "", "you?"]
        messages = [first_message, second_message, third_message]

        result = get_message(messages)

        assert result is False
    
    def test_should_return_original_message(self):
        """
        Test that get_message returns the original message when
        every word was received properly in at least one satellite.
        """
        
        first_message = ["Hello", "how", "", ""]
        second_message = ["", "", "are", ""]
        third_message = ["", "", "", "you?"]
        messages = [first_message, second_message, third_message]

        result = get_message(messages)

        assert result == "Hello how are you?"
