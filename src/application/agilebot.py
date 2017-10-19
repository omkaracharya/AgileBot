import os
import time
import datetime
from bot import Bot
from slackclient import SlackClient

READ_WEBSOCKET_DELAY = 1


def prepare_response(channel, user, message):
    """
    This function calls the service logic for the command entered by the user in Slack
    e.g. msg = "givemystatus 01/21/2017
    :param channel: string containing channel in which the message is sent/to be sent
    :param user: string containing user id who sent the messsage
    :param message: string containing Slack message
    :return: response
    """

    response = ""
    # This contains the first word in the message (should be a valid command ideally)
    original_command = message.split(" ")[0]
    command = original_command.lower()

    if command == "plansprint":
        if len(message.split(" ")) == 1:
            response = "Please provide the start date and the end date."

        elif len(message.split(" ")) == 2:
            response = "Please provide the end date."

        elif len(message.split(" ")) > 3:
            response = "Invalid use of *" + original_command + "*. Please check the usage."

        else:
            # This contains the date
            start_date = message.split(" ")[1]
            end_date = message.split(" ")[2]

            # Check if a valid date is entered
            try:
                start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
                end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")

                # TODO - Check for end_date >= start_date
                #

                response = "*Tentative Sprint Plan for *`" + datetime.datetime.strftime(start_date, "%m/%d/%Y") \
                           + "` *to* `" + datetime.datetime.strftime(end_date, "%m/%d/%Y") + "`"

                # TODO - Plan Sprint
                # response += plan_sprint(start_date, end_date)
                response += "\n```1. Story #1: @omkar.acharya\n2. Story #2: @yvlele```"

            except ValueError:
                # Invalid date
                response = "Enter a valid status date!"

    elif command == "givemystatus":
        if len(message.split(" ")) < 2:
            response = "Please provide the date."

        elif len(message.split(" ")) > 2:
            response = "Invalid use of *" + original_command + "*. Please check the usage."

        else:
            # This contains the date
            status_date = message.split(" ")[1]
            # Check if a valid date is entered
            try:
                status_date = datetime.datetime.strptime(status_date, "%m/%d/%Y")

                # TODO - Check if the entered date is from the past (no future dates)
                #

                response = "Here is your status for " + datetime.datetime.strftime(status_date, "%m/%d/%Y")

                # TODO - User's status update
                # response += give_user_status(user)
                response += "\n`Currently you have no commits.`"

            except ValueError:
                # Invalid date
                response = "Enter a valid status date!"

    elif command == "groombacklog":
        if len(message.split(" ")) != 1:
            response = "Invalid use of *" + original_command + "*. Please check the usage."

        else:
            response = "Tentative Backlog Grooming: "

            # TODO - Groom Backlog
            # response += groom_backlog()
            response += "```1. Story #1: Points 5\n2.Story #2. Points 10```"

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


def get_bot_credentials():
    """
    This function gets the environmental variables set for the bot details
    :return: bot_id, bot_token
    """
    bot_id = os.environ.get("AGILEBOT_ID")
    bot_token = os.environ.get("AGILEBOT_TOKEN")
    return bot_id, bot_token


# Main function
if __name__ == "__main__":
    # Initializae the bot
    bot_id, bot_token = get_bot_credentials()
    bot_name = "agilebot"

    # Invalid bot credentials
    if not bot_id:
        print("Set AGILEBOT_ID as an environment variable")
        exit()

    if not bot_token:
        print("Set AGILEBOT_TOKEN as an environment variable")
        exit()

    # Create a Bot object
    agilebot = Bot(bot_id, bot_token, bot_name)

    # Create a Stack client
    slack_client = SlackClient(agilebot.token)

    if slack_client.rtm_connect():
        print(agilebot.name + " is active on Slack..")
        # Always stay active
        while True:
            channel, user, message = get_messages(slack_client.rtm_read(), agilebot.address)
            if channel and user and message:
                # Response to the user
                response = prepare_response(channel, user, message)
                # TODO - Look for user_id to user_name dictionary
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

                # TODO - Use interactive Slack message buttons
                # TODO - Use ephemeral messages depending on the command
                # slack_client.api_call("chat.postEphemeral", channel=channel, text=response, as_user=True, user="U6WJKJEUD")

            elif channel and user:
                response = "*Usage:* `plansprint startdate enddate` or `givemystatus statusdate` or `groombacklog`" \
                           "\n*Date format:* MM/DD/YYYY"
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed..")
