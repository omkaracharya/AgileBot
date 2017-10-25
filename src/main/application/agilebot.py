# The main application that runs the agilebot.
import os
import time

from main.application.action_builder import ActionBuilder, get_usage
from main.data.bot import Bot
from main.data.environment import set_env
from main.data.validator import is_valid_bot, validate_message
from main.service.slack import get_connection

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


def execute_bot(slack_client, agilebot):
    # Always stay active
    while True:
        channel, user, message = get_messages(slack_client.rtm_read(), agilebot.address)
        if channel and user and message:
            command, request = validate_message(message)
            if command:
                # Response to the user
                action = ActionBuilder.build(command)
                response = action.get_response(user, request)
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
            execute_bot(slack_client, agilebot)
        else:
            print("Connection failed..")


# Main function
if __name__ == "__main__":
    # Initialize environment
    set_env()
    run()
