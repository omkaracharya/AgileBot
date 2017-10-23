import main.data.environment as env
from pyral import Rally
from main.data.environment import get_env

class AgileFactory(object):
    #create based on if mocking is on or not

    def connect():
        server = get_env("RALLY_SERVER")
        user = get_env("RALLY_USER")
        password = get_env("RALLY_PASSWORD")
        apikey = get_env("RALLY_APIKEY")
        rally = Rally(server, user, password, apikey)
        return rally

    connect = staticmethod(connect)
    def factory():
        mock = env.get_env('MOCK')
        if mock and mock == 'True':
            return FakeRally()
        return AgileFactory.connect()

    factory = staticmethod(factory)

class FakeRally():

    def get(self, *args, **kwargs):
        return "\n1. Story #1: Points 5\n" \
               "2. Story #2: Points 10\n" \
               "3. Story #3: Points 8"