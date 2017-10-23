from datetime import datetime

from main.data.commands import GROOMBACKLOG
from main.service.rally import groom_backlog


class GroomBacklog:
    def __init__(self):
        self.date = datetime.today()
        self.command = GROOMBACKLOG
        self.RESPONSE_HEADER = "Groomed Backlog:"
        self.INVALID_RESPONSE = "\nNo stories in backlog to groom."

    def get_response(self, user, request):
        # TODO: Implement service/ read from mock file
        if request:
            date = request[0]
            try:
                self.date = datetime.strptime(date, "%m/%d/%Y")
            except Exception as e:
                self.date = datetime.today()

        response = self.RESPONSE_HEADER
        backlog = groom_backlog(self.date)
        if backlog:
            response += backlog
        else:
            response += self.INVALID_RESPONSE
        return response
