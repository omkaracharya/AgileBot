# Use Case: groom backlog

from datetime import datetime

from main.application.authority import get_action_authorized
from main.data.commands import GROOMBACKLOG
from main.service.rally import get_ungroomed_stories


class GroomBacklog:
    def __init__(self):
        self.date = datetime.today()
        self.command = GROOMBACKLOG
        self.RESPONSE_HEADER = "Groomed Backlog:"
        self.INVALID_RESPONSE = "\nNo stories in backlog to groom."

    def get_response(self, user, all_users, request, rally):
        # TODO: Implement service/ read from mock file
        if request:
            date = request[0]
            try:
                self.date = datetime.strptime(date, "%m/%d/%Y")
            except Exception as e:
                self.date = datetime.today()

        response = self.RESPONSE_HEADER
        backlog = get_ungroomed_stories(self.date)
        perform_action = get_action_authorized(self, self.groom)

        if backlog:
            for story in backlog:
                perform_action(story)

            response += '\n' + '\n'.join(
                ['Story #' + story.FormattedID + ': ' + story.Name + ' (Points: ' + str(story.PlanEstimate) + ')' for
                 story in
                 backlog])
        else:
            response += self.INVALID_RESPONSE
        return response

    # TODO : business logic to assign points
    def groom(self):
        pass
