from pyral import Rally
from main.data.environment import get_env


def connect():
    server = get_env("RALLY_SERVER")
    user = get_env("RALLY_USER")
    password = get_env("RALLY_PASSWORD")
    apikey = get_env("APIKEY")
    rally = Rally(server, user, password, apikey)


def get_projects(rally):
    for workspace in rally.getWorkspaces():
        print(workspace.oid, workspace.Name)
        projects = rally.getProjects(workspace=workspace.Name)
        for project in projects:
            print(project.oid, project.Name)


def get_users(rally):
    for user in rally.getAllUsers():
        print(user.oid, user.Name, user.UserName, user.Role, user.UserProfile.TimeZone)


def groom_backlog():
    # TODO: Implement service/ read from mock file
    return "\n1. Story #1: Points 5\n2. Story #2: Points 10\n3. Story #3: Points 8\n"


def plan_sprint(start_date, end_date):
    # TODO: Implement service/ read from mock file
    return "\n1. Story #1: @omkar.acharya\n2. Story #2: @yvlele"
