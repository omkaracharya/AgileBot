import json
import re
from urllib.parse import unquote_plus

from flask import Flask, request
from slackclient.client import SlackClient

from main.application.action_builder import ActionBuilder
from main.data.environment import get_env
from main.service.slack import get_slackclient

app = Flask(__name__)


def parse_request(request):
    """
    Parse the Slack POST request.
    """
    payload = request.get_data()
    payload = unquote_plus(payload.decode('utf-8'))
    payload = re.sub('payload=', '', payload)
    payload = payload.replace('\\u00a0', '\\n')
    payload = json.loads(payload)
    return payload


@app.route("/slack/message_actions", methods=["POST"])
def post_slack():
    payload = parse_request(request)
    print(payload)
    slack_client = get_slackclient()
    channel = payload['channel']['id']
    if payload['actions'][0]['name'] == 'yes':
        info = payload['actions'][0]['value']
        info = info.split(';')
        command = info[0]
        state = int(info[1])
        action = ActionBuilder.build(command)
        response = action.execute(state)
        print(slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response,
            as_user=True
        ))
        return "Done!"
    else:
        print((SlackClient(get_env("SLACK_TOKEN")).api_call(
            "chat.delete",
            channel=channel,
            ts=payload['actions'][0]['value'],
        )))
        return "No problem, let me know if you need anything else."
