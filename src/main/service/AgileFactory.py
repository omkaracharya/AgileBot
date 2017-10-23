import main.data.environment as env
from pyral import Rally

class AgileFactory(object):
    #create based on if mocking is on or not
    def factory():
        mock = env.get_env('MOCK')
        if mock:
            return FakeRally()
        return Rally()
    factory = staticmethod(factory)

class FakeRally(Rally):

    def __init__(self):
        pass