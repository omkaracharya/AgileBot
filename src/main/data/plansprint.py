# Use case: plan sprint

from main.application.authority import get_action_authorized
from main.data.commands import PLANSPRINT
from main.data.validator import get_valid_date
from main.service.rally import get_stories_for_sprint


class PlanSprint:
    def __init__(self):
        self.command = PLANSPRINT
        self.RESPONSE_HEADER = "Tentative Sprint Plan for "
        self.INVALID_RESPONSE = "\nNo stories in sprint to plan."

    # TODO : business logic to assign owner to a story
    def plan(self, story):
        pass

    def get_response(self, user, request):
        parse_date = None
        if request:
            parse_date = request[0]
        start_date = get_valid_date(parse_date)
        response = self.RESPONSE_HEADER + start_date.strftime("%m/%d/%Y")
        stories = get_stories_for_sprint(start_date)
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
