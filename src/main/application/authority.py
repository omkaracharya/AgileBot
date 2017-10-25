# Authority that checks for authorization based on environment. Used for mocking purposes.

import json
import os

from main.data.commands import PLANSPRINT, GIVEMYSTATUS, GROOMBACKLOG
from main.data.environment import get_env


# Currently used for Selenium and mocking purposes
def should_mock():
    mock = get_env('MOCK')
    return mock and mock == 'True'


def get_action_authorized(action, proposal):
    strategy = proposal
    if should_mock():
        strategies = {PLANSPRINT: fake_plan, GROOMBACKLOG: fake_groom,
                      GIVEMYSTATUS: fake_give}
        strategy = strategies[action.command]
    return strategy


def is_authorized_date(date):
    if should_mock() and date.day % 2 == 0:
        return False
    return True


def get_authorized_connection_or_permission():
    if should_mock():
        return FakeRally()
    return None


def fake_plan(story):
    if story.Owner.DisplayName == 'amwat':
        story.Owner.DisplayName = 'yvlele'


def fake_groom(story):
    story.PlanEstimate = int(story.FormattedID[-1])


def fake_give():
    pass


class FakeRallyRESTResponse:
    def __init__(self, FormattedID, Name, PlanEstimate, Owner=None):
        self.FormattedID = FormattedID
        self.Name = Name
        self.PlanEstimate = PlanEstimate
        self.Owner = FakeRallyUser(Owner)


class FakeRallyUser:
    def __init__(self, Owner):
        self.DisplayName = Owner['_refObjectName'] if Owner else ''


class FakeRally:
    """
        Fake object that overrides the `get()` method of Rally Class and
        returns a curated response using mock data
    """

    def get(self, *args, **kwargs):
        mock_data_repo = {'FormattedID,Name,PlanEstimate,Owner': '../data/mock/sprint_plan.json',
                          'FormattedID,Name,PlanEstimate': '../data/mock/backlog_stories.json'}

        file_path = mock_data_repo[kwargs['fetch']]
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            stories = json.load(f)
        return [FakeRallyRESTResponse(story['FormattedID'],
                                      story['Name'],
                                      story['PlanEstimate'],
                                      story['Owner'] if 'Owner' in story else None) for story in stories]