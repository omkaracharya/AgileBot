# Validator for message and authentication tokens.

from main.application.action_builder import get_supported_actions


def is_valid_bot(bot_id, bot_token):
    # Invalid bot credentials
    if not bot_id:
        print("Set AGILEBOT_ID as an environment variable")
        return False

    if not bot_token:
        print("Set AGILEBOT_TOKEN as an environment variable")
        return False

    return True


def validate_message(message):
    # This contains the first word in the message (should be a valid command ideally)
    split_message = message.split(" ")
    command = split_message[0].lower()
    request = split_message[1:]
    if command in get_supported_actions():
        return command, request
    return None, None
