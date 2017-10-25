
from main.application.authority import is_authorized_date, should_mock
import os
import json
from datetime import datetime

class VCSFactory:
    # create based on if mocking is on or not

    @staticmethod
    def factory():
        grant = should_mock()
        if grant and grant == True:
            return FakeGitRepository()
        return

class GitRepository:

    def __init__(self):
        pass

class FakeGitRepository:

    def get_commits(self, user, date):
        file_path = ('../data/mock/git_commits.json')
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            commits = json.load(f)
        return [(datetime
                    .strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
                    .strftime("%m/%d/%Y %H:%M:%S"),
                 commit['commit']['message'])
                for commit in commits]


def get_commits(user, date):
    if date and not is_authorized_date(date):
        return None

    github = VCSFactory.factory()
    return github.get_commits(user, date)

