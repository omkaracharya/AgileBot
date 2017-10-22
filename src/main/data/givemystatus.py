from datetime import datetime

from main.service.github import get_commits


class StatusUpdate:
    def __init__(self):
        self.date = datetime.today()

    def get_response(self, user, request):
        if request:
            status_date = request[0]
            try:
                self.date = datetime.strptime(status_date, "%m/%d/%Y")
            except Exception as e:
                self.date = datetime.today()

        response = "Here is your status for " + self.date.strftime("%m/%d/%Y")
        # TODO - User's status update
        # response += give_user_status(user)
        response += get_commits(user, self.date)
        return response
