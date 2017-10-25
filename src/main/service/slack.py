# Service that interacts with Slack.

from slackclient import SlackClient


def get_connection(bot_token):
    # Create a Stack client
    return SlackClient(bot_token)
