# Service that interacts with Rally.

from pyral import Rally

from main.application.authority import is_authorized_date
from main.data.agilefactory import get_instance
from main.data.environment import get_env


def connect(rally):
    server = get_env("RALLY_SERVER")
    user = get_env("RALLY_USER")
    password = get_env("RALLY_PASSWORD")
    apikey = get_env("RALLY_APIKEY")
    rally = Rally(server, user, password, apikey)
    return rally


def get_projects(rally):
    for workspace in rally.getWorkspaces():
        print("Workspace: " + workspace.Name)
        projects = rally.getProjects(workspace=workspace.Name)
        for project in projects:
            print(project.oid, project.Name)


def get_users(rally):
    for user in rally.getAllUsers():
        print(user.oid, user.Name, user.UserName, user.Role)


def get_ungroomed_stories(start_date):
    if start_date and is_authorized_date(start_date):
        rally = get_instance()
        # Get the pending stories without any points assigned
        fields = "FormattedID,Name,PlanEstimate"
        criterion = "PlanEstimate = null"
        stories = rally.get('UserStory', fetch=fields, query=criterion)
        return stories
    return None


def get_stories_for_sprint(start_date):
    if not is_authorized_date(start_date):
        return None
    rally = get_instance()
    fields = "FormattedID,Name,PlanEstimate,Owner"
    criterion = "PlanEstimate != null"
    stories = rally.get('UserStory', fetch=fields, query=criterion)
    return stories
