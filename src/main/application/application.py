# The main application that runs the agilebot.
import os
import time

from main.application.action_builder import ActionBuilder, get_usage
from main.application.agilefactory import get_instance
from main.data.bot import Bot
from main.data.environment import set_env
from main.data.validator import is_valid_bot, validate_message, is_valid_user
from main.service.slack import get_connection
from main.data.user import User

from datetime import datetime

READ_WEBSOCKET_DELAY = 1


def get_messages(slack_rtm_output, bot_address):
    """
    This function parses the Stack message
    :param slack_rtm_output: Slack message object
    :param bot_address: string containing how the bot is addressed e.g. <@BOT_ID>
    :return: command, user, message
    """

    messages = slack_rtm_output
    # Check for valid messages
    if messages:
        # Parse command and channel
        for message in messages:
            if message and 'text' in message and bot_address in message['text']:
                channel = message['channel']
                user = message['user']
                text = message['text']
                message = text.split(bot_address)[1].strip()
                return channel, user, message
    return None, None, None


def execute_bot(slack_client, rally, agilebot, all_users):
    # Always stay active
    while True:
        channel, user, message = get_messages(slack_client.rtm_read(), agilebot.address)
        if channel and user and message:
            command, request = validate_message(message)
            if command:
                # Response to the user
                action = ActionBuilder.build(command)
                response = action.get_response(user, all_users, request, rally)
                user_name = "<@" + user + "> "
                response = user_name + response

                # TODO - Use interactive Slack message buttons
                # TODO - Use ephemeral messages depending on the command
                # slack_client.api_call("chat.postEphemeral", channel=channel, text=response, as_user=True, user="U6WJKJEUD")
            else:
                response = get_usage()
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        time.sleep(READ_WEBSOCKET_DELAY)


def get_bot_credentials():
    """
    This function gets the environmental variables set for the bot details
    :return: bot_id, bot_token
    """
    bot_id = os.environ.get("AGILEBOT_ID")
    bot_token = os.environ.get("AGILEBOT_TOKEN")
    return bot_id, bot_token


def run():
    # Initialize the bot
    bot_id, bot_token = get_bot_credentials()
    bot_name = "agilebot"

    if is_valid_bot(bot_id, bot_token):
        # Create a Bot object
        agilebot = Bot(bot_id, bot_token, bot_name)
        slack_client = get_connection(bot_token)
        if slack_client.rtm_connect():
            print("'" + agilebot.name + "' is active on Slack..")
            rally = get_instance()
            all_users = get_user_data(slack_client, rally)
            execute_bot(slack_client, rally, agilebot, all_users)
        else:
            print("Connection failed..")


def get_user_data(slack_client, rally):
    # Populate User Data
    all_users = list()
    user_list = slack_client.api_call("users.list")
    for user in user_list['members']:
        if is_valid_user(user):
            user_id = user['id']
            user_email = user['profile']['email']
            user_tz = user['tz']
            all_users.append(User(user_id, user_email, user_tz))
    return all_users


# Main function
if __name__ == "__main__":
    # Initialize environment
    set_env()
    run()
