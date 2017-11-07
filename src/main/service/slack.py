# Service that interacts with Slack.

from slackclient import SlackClient
import os

slack_client = None


def get_slackclient():
    if not slack_client:
        # Create a Stack client
        _, bot_token = get_bot_credentials()
        return SlackClient(bot_token)
    return slack_client


def get_bot_credentials():
    """
    This function gets the environmental variables set for the bot details
    :return: bot_id, bot_token
    """
    bot_id = os.environ.get("AGILEBOT_ID")
    bot_token = os.environ.get("AGILEBOT_TOKEN")
    return bot_id, bot_token
