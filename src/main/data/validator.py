# Validator for message and authentication tokens.

from datetime import datetime

from main.data.commands import get_supported_commands


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
    if command in get_supported_commands():
        return command, request
    return None, None


def get_valid_date(date):
    try:
        validated_date = datetime.strptime(date, "%m/%d/%Y")
        return validated_date
    except Exception as e:
        return datetime.today()


def is_valid_user(user):
    return not user['is_bot'] and user['name'] != 'slackbot' and not user['deleted']