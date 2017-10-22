from main.service.rally import groom_backlog


class GroomBacklog:
    def __init__(self):
        pass

    def get_response(self, user, request):
        response = "Groomed Backlog:"
        response += groom_backlog()
        return response
