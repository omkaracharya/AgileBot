import os

from pyral import Rally

SERVER = "rally1.rallydev.com"
# WORKSPACE = "Test Workspace"
# PROJECT = "AgileBot"

USER = os.environ.get("RALLY_USERNAME")
PASSWORD = os.environ.get("RALLY_PASSWORD")
APIKEY = os.environ.get("RALLY_APIKEY")
# rally = Rally(SERVER, USER, PASSWORD, apikey=APIKEY, workspace=WORKSPACE, project=PROJECT)
rally = Rally(SERVER, USER, PASSWORD, apikey=APIKEY)


def get_projects():
    for workspace in rally.getWorkspaces():
        print(workspace.oid, workspace.Name)
        projects = rally.getProjects(workspace=workspace.Name)
        for project in projects:
            print(project.oid, project.Name)


def get_users():
    for user in rally.getAllUsers():
        print(user.oid, user.Name, user.UserName, user.Role, user.UserProfile.TimeZone)


get_projects()
get_users()
