import os
import time
import datetime
from slackclient import SlackClient

# Slack bot name
BOT_NAME = "agilebot"

# Get the bot ID
BOT_ID = os.environ.get("BOT_ID")
BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# Referring the bot as @agilebot
AT_BOT = "<@" + BOT_ID + ">"

# Expected command
EXAMPLE_COMMAND = "givemystatus"


def handle_command(msg, channel):
    '''
    This function calls the service logic for the command entered by the user in Slack
    e.g. msg = "givemystatus 01/21/2017
    :param msg: string containing Slack message
    :param channel: string containing channel in which the message is sent/to be sent
    :return: -
    '''
    response = ""
    # This contains the first word in the message (should be a valid command ideally)
    command = msg.split(" ")[0]
    # This contains the date
    status_date = msg.split(" ")[1]
    # If valid command is entered
    if command == EXAMPLE_COMMAND:
        # Date's validity check
        try:
            status_date = datetime.datetime.strptime(status_date, "%m/%d/%Y")
            response = "Here is your status for " + datetime.datetime.strftime(status_date,
                                                                               "%m/%d/%Y") + ":\n```Currently you have no commits.```"
            # TODO - User's status update
            # response += give_user_status(user_id)
        except ValueError:
            # Invalid date
            response = "Enter a valid status date!"
    else:
        # Invalid command
        response = "Try using: *" + EXAMPLE_COMMAND + " mm/dd/yyyy*"

    # Response to the user
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    # TODO - Use interactive Slack message buttons and ephemeral messages
    # slack_client.api_call("chat.postEphemeral", channel=channel, text=response, as_user=True, user="U6WJKJEUD")


def parse_slack_output(slack_rtm_output):
    '''
    This function parses the Stack message
    :param slack_rtm_output: Slack message object
    :return: command, channel
    '''
    output_list = slack_rtm_output
    # Check for valid messages
    if output_list and len(output_list) > 0:
        # Parse command and channel
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


# def get_bot_id(BOT_NAME):
#     api_call = slack_client.api_call("users.list")
#     if api_call.get("ok"):
#         users = api_call.get("members")
#         for user in users:
#             if "name" in user and user.get("name") == BOT_NAME:
#                 return user.get("id"))
#     else:
#         return None


# Create a Stack client
slack_client = SlackClient(BOT_TOKEN)

# Main function
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
