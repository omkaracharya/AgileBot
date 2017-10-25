from pyral import Rally

from main.application.authority import Authority
from main.data.environment import get_env


class AgileFactory:
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
        grant = Authority.get_authorized_connection_or_permission()
        if grant:
            return grant
        return AgileFactory.connect()
