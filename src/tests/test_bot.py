import sys
# import request
from unittest.mock import patch
# from nose.tools import assert_true
import main.service.rally as ralley_service



# @patch('agilebot.os')
# def test_env(mock_os):
#     BOT_ID = mock_os.environ.get("BOT_ID")
#     mock_os.environ.get.assert_called_with("BOT_ID")

class User:

    def __init__(self, oid, username, name, role):
        self.oid = oid
        self.Name = name
        self.UserName = username
        self.Role = role

@patch('pyral.Rally')
def test_rally_get_users(mock_rally):
    user1 = User(1, "klal", "Kishan Lal", "Boss")
    user2 = User(2, "vkhanna", "Vinod Khanna", "Sheth")
    mock_rally.getAllUsers.return_value = [user1, user2]
    ralley_service.get_users(mock_rally)

