from pyral import Rally

from main.data.environment import get_env
from main.service import AgileFactory


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

    rally = AgileFactory.AgileFactory.factory()
    # Get the pending stories without any points assigned
    #
    story_assignment = rally.get('UserStory', fetch=True, query='State != "Closed"')

    #return "\n1. Story #1: Points 5\n2. Story #2: Points 10\n3. Story #3: Points 8"
    return story_assignment


def plan_sprint(start_date):
    # TODO: Implement service/ read from mock file
    if start_date.day % 2 == 0:
        return None
    return "\n1. Story #1: @omkar.acharya\n2. Story #2: @yvlele"
