import json


def is_there_any_unknown_message(satellites_info):
    """
    Determine whether there are satellites 
    that have not receive any message yet.

    Args:
        - satellites_info (QuerySet): all the information already known about the satellites.

    Returns:
        bool:
            - True if there is at least one satellite that has not received any message.
            - False otherwise.
    """
    return satellites_info.filter(message_received__isnull=True).count() > 0


def get_messages(satellites_info):
    """
    Retrieve the messages received by every satellite.

    Args:
        - satellites_info (QuerySet): all the information already known about the satellites.

    Returns:
        list[str]: messages received by the satellites.
    """
    messages = satellites_info.values_list('message_received')
    return [
        json.loads(message[0])
        for message in messages
    ]
