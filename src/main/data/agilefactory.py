import json
import os
import random

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
    def __init__(self, FormattedID, Name, PlanEstimate, Owner=None):
        self.FormattedID = FormattedID
        self.Name = Name
        self.PlanEstimate = PlanEstimate or random.choice([3,5,8,13,21])
        self.Owner = FakeRallyUser(Owner)

class FakeRallyUser:
    def __init__(self, Owner):
        self.DisplayName = Owner['_refObjectName'] if Owner else ''

class FakeRally():
    """
        Fake object that overrides the `get()` method of Rally Class and
        returns a curated response using mock data
    """
    def get(self, *args, **kwargs):
        # print(kwargs['fetch'])
        mock_data_repo =  {'FormattedID,Name,PlanEstimate,Owner' : '../data/mock/sprint_plan.json',
                           'FormattedID,Name,PlanEstimate' : '../data/mock/backlog_stories.json'}

        file_path = mock_data_repo[kwargs['fetch']]
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            stories = json.load(f)
        return [FakeRallyRESTResponse(story['FormattedID'],
                                      story['Name'],
                                      story['PlanEstimate'],
                                      story['Owner'] if 'Owner' in story else None) for story in stories]
