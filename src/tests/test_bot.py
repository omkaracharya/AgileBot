import sys
# import request
from unittest.mock import patch
# from nose.tools import assert_true

sys.path.append("../src/application/main")


@patch('agilebot.os')
def test_env(mock_os):
    BOT_ID = mock_os.environ.get("BOT_ID")
    mock_os.environ.get.assert_called_with("BOT_ID")

# @mock.patch('agilebot.slack_client')
# def test_handle_command(mock_slack_client):
#     agilebot.handle_command("givemystatus 04/20/2018", None)
#     mock_slack_client.api_call.assert_called()