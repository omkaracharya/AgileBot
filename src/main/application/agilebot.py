import datetime
import os
import time

from main.application.action_builder import get_action, get_usage
from main.data.bot import Bot
from main.data.environment import set_env
from main.data.validator import is_valid_bot, validate_message
from main.service.slack import get_connection

READ_WEBSOCKET_DELAY = 1


def prepare_response(command, message):
    """
    This function calls the service logic for the command entered by the user in Slack
    e.g. msg = "givemystatus 01/21/2017
    :param message: string containing Slack message
    :return: response
    """

    response = ""

    if command == "plansprint":
        if len(message.split(" ")) == 1:
            response = "Please provide the start date and the end date."

        elif len(message.split(" ")) == 2:
            response = "Please provide the end date."

        elif len(message.split(" ")) > 3:
            response = "Invalid use of *" + command + "*. Please check the usage."

        else:
            # This contains the date
            start_date = message.split(" ")[1]
            end_date = message.split(" ")[2]

            # Check if a valid date is entered
            try:
                start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
                end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")

                if start_date > end_date:
                    response = "Start date should be before end date."
                    return response

                response = "*Tentative Sprint Plan for *" + datetime.datetime.strftime(start_date, "%m/%d/%Y") \
                           + " *to* " + datetime.datetime.strftime(end_date, "%m/%d/%Y")

                # TODO - Plan Sprint
                # response += plan_sprint(start_date, end_date)
                response += "\n1. Story #1: @omkar.acharya\n2. Story #2: @yvlele"

            except ValueError:
                # Invalid date
                response = "Enter a valid status date!"

    elif command == "groombacklog":
        if len(message.split(" ")) != 1:
            response = "Invalid use of *" + command + "*. Please check the usage."

        else:
            response = "Tentative Backlog Grooming: "

            # TODO - Groom Backlog
            # response += groom_backlog()
            response += "```1. Story #1: Points 5\n2. Story #2. Points 10```"

    else:
        # Invalid command
        response = "*Usage:* `plansprint startdate enddate` or `givemystatus statusdate` or `groombacklog`" \
                   "\n*Date format:* MM/DD/YYYY"

    return response


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
                action = get_action(command)
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
            print(agilebot.name + " is active on Slack..")
            execute_bot(slack_client, agilebot)
        else:
            print("Connection failed..")


# Main function
if __name__ == "__main__":
    # Initialize environment
    set_env()
    run()
