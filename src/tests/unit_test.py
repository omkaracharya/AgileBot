# Unit Tests.

from datetime import datetime
from unittest.mock import patch

from nose.tools import assert_true

import main.service.github as github
import main.service.rally as ralley_service
from main.data.environment import set_env


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


# @patch('pyral.Rally')
# def test_rally_get_workspace(mock_rally):
#     set_env()
#     rally = None
#     rally = ralley_service.connect(rally)
#     ralley_service.get_projects(rally)

def test_get_stories():
    set_env()
    ralley_service.get_ungroomed_stories(None)


def test_get_commits_with_valid_date():
    set_env()
    user = 'kpohe'
    strdate = '11/11/2017'
    date = datetime.strptime(strdate, "%m/%d/%Y")
    assert_true(github.get_commits(user, "", date, "") != None)


def test_get_commits_with_unauthorized_date():
    set_env()
    user = 'kobi'
    strdate = '02/28/2000'
    date = datetime.strptime(strdate, "%m/%d/%Y")
    from main.application.authority import should_mock
    if should_mock() == True:
        assert_true(github.get_commits(user,"", date, "") == None)
