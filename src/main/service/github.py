from main.application.authority import is_authorized_date, should_mock
import os
import json
from datetime import datetime, timedelta
import urllib


class VCSFactory:
    # create based on if mocking is on or not

    @staticmethod
    def factory():
        grant = should_mock()
        if grant:
            return FakeGitRepository()
        return GitRepository()


class GitRepository:
    def __init__(self):
        self.url = "https://api.github.com/repos/omkaracharya/VidScribe/commits?since={}&until={}&author={}"

    def get_commits(self, user, date):
        # TODO: get author from {slack_id:email} dictionary
        slack_to_email_dict = dict()
        # print(user)
        slack_to_email_dict[user] = "acharyaomkar01@gmail.com"
        iso_timestamp = "T00:00:00Z"

        since = datetime.strftime(date, "%Y-%m-%d") + iso_timestamp
        until = datetime.strftime(date + timedelta(days=1), "%Y-%m-%d") + iso_timestamp
        author = slack_to_email_dict[user]

        request = urllib.request.Request(self.url.format(since, until, author))
        response = urllib.request.urlopen(request)
        commits = json.loads(response.read().decode('utf-8'))
        return format_commits(commits)


class FakeGitRepository:
    def get_commits(self, user, date):
        file_path = ('../data/mock/git_commits.json')
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            commits = json.load(f)
        return format_commits(commits)


def get_commits(user, date):
    if date and not is_authorized_date(date):
        return None

    github = VCSFactory.factory()
    return github.get_commits(user, date)


def format_commits(commits):
    return [(datetime
             .strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
             .strftime("%m/%d/%Y %H:%M:%S"),
             commit['commit']['message'])
            for commit in commits]
