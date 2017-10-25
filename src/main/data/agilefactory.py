# Factory method that returns the Rally object after connection or corresponding mock object.
from pyral import Rally

from main.application.authority import get_authorized_connection_or_permission
from main.data.environment import get_env


class AgileFactory:
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
        grant = get_authorized_connection_or_permission()
        if grant:
            return grant
        return AgileFactory.connect()
