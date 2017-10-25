# Use case: plan sprint

from datetime import datetime

from main.application.authority import get_action_authorized
from main.data.commands import PLANSPRINT
from main.service.rally import get_stories_for_sprint


class PlanSprint:
    def __init__(self):
        self.start_date = datetime.today()
        self.command = PLANSPRINT
        self.RESPONSE_HEADER = "Tentative Sprint Plan for "
        self.INVALID_RESPONSE = "\nNo stories in sprint to plan."

    # TODO : business logic to assign owner to a story
    def plan(self, story):
        pass

    def get_response(self, user, request):
        if request:
            start_date = request[0]
            try:
                self.start_date = datetime.strptime(start_date, "%m/%d/%Y")
            except Exception as e:
                self.start_date = datetime.today()

        response = self.RESPONSE_HEADER + self.start_date.strftime("%m/%d/%Y")
        stories = get_stories_for_sprint(self.start_date)
        perform_action = get_action_authorized(self, self.plan)

        if stories:
            for story in stories:
                perform_action(story)

            response += '\n' + '\n'.join(['Story #' + story.FormattedID + ': '
                                          + story.Name + ' (Owner: @' + str(story.Owner.DisplayName)
                                          + ' Points = ' + str(story.PlanEstimate) + ')'
                                          for story in stories])
        else:
            response += self.INVALID_RESPONSE
        return response
