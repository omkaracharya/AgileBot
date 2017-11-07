from flask import Flask, request, make_response, Response
from urllib.parse import unquote_plus
import re
import json

app = Flask(__name__)


def parse_request(request):
    """
    Parse the Slack POST request.
    """
    payload = request.get_data()
    payload = unquote_plus(payload.decode('utf-8'))
    payload = re.sub('payload=', '', payload)
    payload = json.loads(payload)
    return payload


@app.route("/slack/message_actions", methods=["POST"])
def post_slack():
    payload = parse_request(request)
    print(payload)
    if payload['actions'][0]['value'] == 'yes':
        slack_client.api_call(
            "chat.postMessage",
            channel="@omkar.acharya",
            text="Thanks! Your sprint has been planned!",
            as_user=True
        )
        #        confirm()

        return "Done!!!"
    else:
        slack_client.api_call(
            "chat.postEphemeral",
            channel="@omkar.acharya",
            text="I will get back to you!!",
            as_user=True
        )
        return "Hold your horses!"


def confirm():
    # Post a message to a channel, asking users if they want to play a game
    attachments_json = [
        {
            "title": "Plan Sprint for 11/06/2017",
            "callback_id": "123",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "yes",
                    "text": "Yes",
                    "value": "yes",
                    "type": "button",
                },
                {
                    "name": "no",
                    "text": "No",
                    "value": "no",
                    "type": "button",
                }
            ]
        }
    ]

    slack_client.api_call(
        "chat.postMessage",
        channel="@omkar.acharya",
        text="Does this look good?",
        attachments=attachments_json,
        as_user=True
    )
