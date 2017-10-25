from datetime import datetime
import sys
# import request
from unittest.mock import patch
from nose.tools import assert_true
import main.service.rally as ralley_service
from main.data.environment import set_env
import main.service.github as github


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

# @patch('pyral.Rally')
# def test_rally_get_workspace(mock_rally):
#     set_env('../../environment_variables.txt')
#     rally = None
#     rally = ralley_service.connect(rally)
#     ralley_service.get_projects(rally)

def test_get_stories():
    set_env('../../environment_variables.txt')
    ralley_service.get_ungroomed_stories(None)

def test_get_commits_with_valid_date():
    set_env('../../environment_variables.txt')
    user = 'kpohe'
    strdate = '11/11/2017'
    date = datetime.strptime(strdate, "%m/%d/%Y")
    assert_true(github.get_commits(user, date) != None)

def test_get_commits_with_unauthorized_date():
    set_env('../../environment_variables.txt')
    user = 'kobi'
    strdate = '02/28/2000'
    date = datetime.strptime(strdate, "%m/%d/%Y")
    from main.application.authority import should_mock
    if should_mock() == True:
        assert_true(github.get_commits(user, date) == None)
