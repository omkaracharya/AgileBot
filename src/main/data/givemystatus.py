from datetime import datetime

from main.data.commands import GIVEMYSTATUS
from main.service.github import get_commits


class StatusUpdate:
    def __init__(self):
        self.date = datetime.today()
        self.command = GIVEMYSTATUS
        self.RESPONSE_HEADER = "Here is your status for "
        self.INVALID_RESPONSE = "\nCurrently you have no commits."

    def get_response(self, user, request):
        if request:
            status_date = request[0]
            try:
                self.date = datetime.strptime(status_date, "%m/%d/%Y")
            except Exception as e:
                self.date = datetime.today()

        response = self.RESPONSE_HEADER + self.date.strftime("%m/%d/%Y")
        commits = get_commits(user, self.date)
        if commits:
            response += commits
        else:
            response += self.INVALID_RESPONSE
        return response

    def give(self):
        pass
