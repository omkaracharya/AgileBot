from datetime import datetime

from main.service.rally import plan_sprint


class PlanSprint:
    def __init__(self):
        self.start_date = datetime.today()

    def get_response(self, user, request):
        if request:
            start_date = request[0]
            try:
                self.start_date = datetime.strptime(start_date, "%m/%d/%Y")
            except Exception as e:
                self.start_date = datetime.today()

        response = "Tentative Sprint Plan for " + self.start_date.strftime("%m/%d/%Y")
        response += plan_sprint(user, self.start_date)
        return response
