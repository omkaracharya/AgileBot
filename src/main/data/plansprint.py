from datetime import datetime

from main.data.commands import PLANSPRINT
from main.service.rally import plan_sprint


class PlanSprint:
    def __init__(self):
        self.start_date = datetime.today()
        self.command = PLANSPRINT
        self.RESPONSE_HEADER = "Tentative Sprint Plan for "
        self.INVALID_RESPONSE = "\nNo stories in sprint to plan."

    def get_response(self, user, request):
        if request:
            start_date = request[0]
            try:
                self.start_date = datetime.strptime(start_date, "%m/%d/%Y")
            except Exception as e:
                self.start_date = datetime.today()

        response = self.RESPONSE_HEADER + self.start_date.strftime("%m/%d/%Y")
        plan = plan_sprint(self.start_date)
        if plan:
            response += plan
        else:
            response += self.INVALID_RESPONSE
        return response
