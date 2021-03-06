from typing import List


def get_message(messages: List[List[str]]) -> str:
    """Retrieve the original message given a list of messages retrieved in each satellite.

    Args:
        - messages: List of list of words retrieved in each satellite.
            Every item in this argument represents the list of words retrieved in the satellite.
                Every string in the item represents a word retrieved in the satellite.
                    If the string is blank (''), it means that the word wasn't properly retrieved.
    
    Returns:
        A string that represent the original message sent by the transmitter.
    """
    first_message = messages[0]
    second_message = messages[1]
    third_message = messages[2]

    message_length = len(first_message)

    # If the lists don't have the same length, then the original message can not be determined.
    if not (message_length == len(second_message) == len(third_message)):
        raise Exception('The messages received by the satellites does not have the same length.')

    original_message = []
    for i in range(message_length):
        current_word = first_message[i] or second_message[i] or third_message[i]
        # If there's a word that wasn't received by any satellite, 
        # then the original message can not be determined.
        if not (current_word):
            raise Exception('The word at this position could not be received by any satellite.')
        
        # If different satellites receive distinct words at the same position, 
        # then the original message is ambiguous and it can not be determined.
        # So, we create a set of the words that were received at this position,
        # and we expect this set to have only one word.
        non_blank_words_received_in_position_i = {
            word for word 
            in [first_message[i], second_message[i], third_message[i]]
            if word != ""
        }
        if non_blank_words_received_in_position_i != set([current_word]):
            raise Exception('Different words were received by the satellites at this position.')
        
        original_message.append(current_word)
    
    return ' '.join(original_message)
