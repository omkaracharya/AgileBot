# Factory method that returns the Rally object after connection or corresponding mock object.
from pyral import Rally

from main.application.authority import get_authorized_connection_or_permission
from main.data.environment import get_env

rally = None


def connect():
    server = get_env("RALLY_SERVER")
    user = get_env("RALLY_USER")
    password = get_env("RALLY_PASSWORD")
    apikey = get_env("RALLY_APIKEY")
    project = get_env("RALLY_PROJECT") or 'default'
    rally = Rally(server, user, password, apikey,project=project)
    return rally


def get_instance():
    grant = get_authorized_connection_or_permission()
    if grant:
        return grant
    global rally
    if not rally:
        rally = connect()
    return rally
