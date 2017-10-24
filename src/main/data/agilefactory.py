import json
import os

from pyral import Rally

import main.data.environment as env
from main.data.environment import get_env


class AgileFactory(object):
    # create based on if mocking is on or not
    @staticmethod
    def connect():
        server = get_env("RALLY_SERVER")
        user = get_env("RALLY_USER")
        password = get_env("RALLY_PASSWORD")
        apikey = get_env("RALLY_APIKEY")
        rally = Rally(server, user, password, apikey)
        return rally

    @staticmethod
    def factory():
        mock = env.get_env('MOCK')
        if mock and mock == 'True':
            return FakeRally()
        return AgileFactory.connect()


class FakeRallyRESTResponse:
    def __init__(self, FormattedID, Name, PlanEstimate):
        self.FormattedID = FormattedID
        self.Name = Name
        self.PlanEstimate = PlanEstimate


class FakeRally():
    def get(self, *args, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), "../data/mock/backlog_stories.json")) as f:
            stories = json.load(f)
        return [FakeRallyRESTResponse(story['FormattedID'], story['Name'], story['PlanEstimate']) for story in stories]
