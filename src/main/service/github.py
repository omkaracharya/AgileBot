import json
import os
import urllib
from datetime import datetime, timedelta

import pytz

from main.application.authority import is_authorized_date, should_mock
from main.data.environment import get_env


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
        self.commits_request_url = "https://github.ncsu.edu/api/v3/repos/{owner}/{repo}/commits"
        self.branches_request_url = "https://github.ncsu.edu/api/v3/repos/{owner}/{repo}/branches"
        self.commits_filter = "?since={start_date}&until={end_date}&author={author}&sha={sha}"
        self.commits_sha = set()
        self.repo_author = get_env("REPO_AUTHOR")
        self.repo_name = get_env("REPO_NAME")
        self.token = get_env("GITHUB_TOKEN")

    def get_commits(self, user, email, date, tz):
        all_commits = list()
        branches = self.get_branches()
        # Start date - yesterday's 12:00 am
        since = (date - timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat()
        # End date - today's 11:59 pm
        until = date.replace(hour=23, minute=59, second=59).isoformat()
        # GitHub REST API calls to get commits for each branch
        for branch in branches:
            commits_request = urllib.request.Request(
                (self.commits_request_url + self.commits_filter).format(owner=self.repo_author, repo=self.repo_name,
                                                                        start_date=since, end_date=until, author=email,
                                                                        sha=branch["commit"]["sha"]))
            # Add GitHub's authorization token
            commits_request.add_header("Authorization", "token {token}".format(token=self.token))
            # Send the request and store the response containing commit details
            response = urllib.request.urlopen(commits_request)
            # Extract commits from JSON format
            commits = json.loads(response.read().decode('utf-8'))
            for commit in commits:
                if commit["sha"] not in self.commits_sha:
                    all_commits.append(format_commit(commit, branch["name"], tz))
                    self.commits_sha.add(commit["sha"])
        # Return commits to the slack channel
        return all_commits

    def get_branches(self):
        # GitHub REST API call
        branches_request = urllib.request.Request(self.branches_request_url.format(owner=self.repo_author,
                                                                                   repo=self.repo_name))
        # Add GitHub's authorization token
        branches_request.add_header("Authorization", "token {token}".format(token=self.token))
        # Send the request and store the response containing branches and their details
        response = urllib.request.urlopen(branches_request)
        # Extract repos from JSON format
        branches = json.loads(response.read().decode('utf-8'))
        # Return branches
        return branches


class FakeGitRepository:
    def get_commits(self, user, email, date, tz):
        file_path = "../data/mock/git_commits.json"
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            commits = json.load(f)
        return format_commit(commits)


def get_commits(user, email, date, tz):
    if date and not is_authorized_date(date):
        return None

    github = VCSFactory.factory()
    return github.get_commits(user, email, date, tz)


def format_commit(commit, branch, tz):
    dt = pytz.utc.localize(datetime.strptime(commit["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ"))
    local_dt = dt.astimezone(pytz.timezone(tz))
    return (local_dt.strftime("%m/%d/%Y %H:%M:%S"),
            "<" + commit["html_url"] + "|" + commit["commit"]["message"] + "> `(" + branch + ")`")
