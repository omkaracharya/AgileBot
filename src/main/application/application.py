# The main application that runs the agilebot.
import time
from threading import Thread

from main.application.action_builder import ActionBuilder, get_usage
from main.application.http_server import app
from main.data.bot import Bot
from main.data.environment import set_env, get_env
from main.data.user import User
from main.data.validator import is_valid_bot, validate_message, is_valid_user
from main.service.rally import get_user_info_from_email
from main.service.slack import get_slackclient, get_bot_credentials

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
                print(message)
                channel = message['channel']
                user = message['user']
                text = message['text']
                ts = message['ts']
                message = text.split(bot_address)[1].strip()
                return channel, user, message, ts
    return None, None, None, None


def execute_bot(slack_client, agilebot, all_users):
    # Always stay active
    while True:
        channel, user, message, ts = get_messages(slack_client.rtm_read(), agilebot.address)
        if channel and user and message:
            command, request = validate_message(message)
            if command:
                # Response to the user
                action = ActionBuilder.build(command)
                response = action.get_response(user, all_users, request)
                user_name = "<@" + user + "> "
                # response = user_name + response

                # TODO - Use interactive Slack message buttons
                # TODO - Use ephemeral messages depending on the command
                confirm(slack_client, user, channel, response, action.SUCCESS_RESPONSE + '\n' + response, ts)
            else:
                response = get_usage()
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        time.sleep(READ_WEBSOCKET_DELAY)


def confirm(slack_client, user, channel, response, success_response, ts):
    attachments_json = [
        {
            "text": "Does this plan look good?",
            "callback_id": "123",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "yes",
                    "text": "Sure!",
                    "type": "button",
                    "value": success_response,
                    "style": "primary",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                },
                {
                    "name": "no",
                    "text": "No! I have something else in mind",
                    "style": "danger",
                    "type": "button",
                    "value": ts
                }
            ]
        }
    ]

    slack_client.api_call(
        "chat.postEphemeral",
        user=user,
        channel=channel,
        text=response,
        attachments=attachments_json,
        as_user=True
    )


def run():
    # Initialize the bot
    bot_id, bot_token = get_bot_credentials()
    bot_name = "agilebot"

    if is_valid_bot(bot_id, bot_token):
        # Create a Bot object
        agilebot = Bot(bot_id, bot_token, bot_name)
        slack_client = get_slackclient()
        flask_server = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": get_env("FLASK_PORT")})
        flask_server.daemon = True
        flask_server.start()
        # app.run(host='0.0.0.0', port=get_env("FLASK_PORT"))
        if slack_client.rtm_connect():
            print("'" + agilebot.name + "' is active on Slack..")
            all_users = get_user_data(slack_client)
            execute_bot(slack_client, agilebot, all_users)
        else:
            print("Connection failed..")


def get_user_data(slack_client):
    # Populate User Data
    all_users = list()
    user_list = slack_client.api_call("users.list")
    for user in user_list['members']:
        if is_valid_user(user):
            user_id = user['id']
            user_email = user['profile']['email']
            user_tz = user['tz']
            rally_id = get_user_info_from_email(user_email)
            all_users.append(User(user_id, user_email, user_tz, rally_id))
    return all_users


# Main function
if __name__ == "__main__":
    # Initialize environment
    set_env()
    run()
