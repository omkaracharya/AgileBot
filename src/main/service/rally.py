from pyral import Rally

from main.data import agilefactory
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


def groom_backlog(start_date):
    if start_date is not None and start_date.day % 2 == 0:
        return None

    rally = agilefactory.AgileFactory.factory()
    # Get the pending stories without any points assigned
    #
    fields = "FormattedID,Name,PlanEstimate"
    criterion = "PlanEstimate = null"
    stories = rally.get('UserStory', fetch=fields, query=criterion)
    # TODO : business logic to assign points
    response = ['Story #' + story.FormattedID + ': ' + story.Name + ' (Points: ' + str(story.PlanEstimate) + ')' for
                story in
                stories]
    return '\n' + '\n'.join(response)


def plan_sprint(start_date):
    # TODO: Implement service/ read from mock file
    if start_date.day % 2 == 0:
        return None
    return "\n1. Story #1: @omkar.acharya\n2. Story #2: @yvlele"
