from main.application.authority import is_authorized_date, should_mock
from main.data.environment import get_env
import os
import json
from datetime import datetime, timedelta
import urllib
from dateutil import tz
import pytz


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
        self.url = "https://github.ncsu.edu/api/v3/repos/{}/{}/commits"
        self.filter = "?since={}&until={}&author={}"

    def get_commits(self, user, email, date, tz):
        repo_author = "oachary"
        repo_name = "AgileBotTest"
        TOKEN = get_env("GITHUB_TOKEN")

        # Start date - yesterday's 12:00 am
        since = (date - timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat()
        # End date - today's 11:59 pm
        until = date.replace(hour=23, minute=59, second=59).isoformat()
        # GitHub REST API call
        request = urllib.request.Request((self.url + self
                                          .filter).format(repo_author, repo_name, since, until, email))
        # Add GitHub's authorization token
        request.add_header("Authorization", "token {}".format(TOKEN))
        # Send the request and store the response containing commit details
        response = urllib.request.urlopen(request)
        # Extract commits from JSON format
        commits = json.loads(response.read().decode('utf-8'))
        # Return commits to the slack channel
        return format_commits(commits, tz)


class FakeGitRepository:
    def get_commits(self, user, email, date, tz):
        file_path = "../data/mock/git_commits.json"
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            commits = json.load(f)
        return format_commits(commits)


def get_commits(user, email, date, tz):
    if date and not is_authorized_date(date):
        return None

    github = VCSFactory.factory()
    return github.get_commits(user, email, date, tz)


def format_commits(commits, tz):
    dt_commits = []
    for commit in commits:
        dt = pytz.utc.localize(datetime.strptime(commit["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ"))
        local_dt = dt.astimezone(pytz.timezone(tz))
        dt_commits.append((local_dt.strftime("%m/%d/%Y %H:%M:%S"), commit["commit"]["message"]))
    return dt_commits
