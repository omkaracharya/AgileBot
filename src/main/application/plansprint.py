# Use case: plan sprint
from random import randint

from main.application.authority import get_action_authorized
from main.application.authority import is_authorized_date
from main.data.commands import PLANSPRINT
from main.data.validator import get_valid_date
from main.service.rally import get_stories_for_sprint, get_user_capacities_for_iteration, get_iteration_by_date, \
    update_story_assignment


class PlanSprint:
    def __init__(self):
        self.command = PLANSPRINT
        self.RESPONSE_HEADER = "Sprint Plan for "
        self.INVALID_RESPONSE = "\nNo stories in sprint to plan."
        self.SUCCESS_RESPONSE = "Your sprint has been planned!"
        self.states = dict()

    # Assigns story to the least developer with enough capacity and least relative load
    def plan(self, iteration, stories):
        user_capacities = [user_capacity for user_capacity in get_user_capacities_for_iteration(iteration.oid)]
        if user_capacities and len(user_capacities) > 0:
            stories.sort(key=lambda x: x.PlanEstimate, reverse=True)
            for story in stories:
                user_capacities.sort(key=lambda x: x.TaskEstimates / x.Capacity)
                for user_capacity in user_capacities:
                    if user_capacity.Capacity - user_capacity.TaskEstimates >= story.PlanEstimate:
                        story.Owner = user_capacities[0].User
                        user_capacities[0].TaskEstimates += story.PlanEstimate
        state = randint(1, 1000000)
        while state in self.states:
            state = randint(1, 1000000)
        self.states[state] = stories
        return state

    def execute(self, state):
        if not state:
            return self.INVALID_RESPONSE
        print(self.states)
        stories = self.states.pop(state)
        print("Performed action!")
        update_story_assignment(stories)
        print(self.states)
        print(story.details() for story in stories)
        response = self.SUCCESS_RESPONSE + "\nFinal Sprint Plan:"
        response += '\n' + '\n'.join(['Story #' + story.FormattedID + ': '
                                      + story.Name + ' (Assignee: ' + (str(
            story.Owner.DisplayName) if story.Owner else 'None')
                                      + ' Points = ' + str(story.PlanEstimate) + ')'
                                      for story in stories])
        return response

    def get_response(self, user, all_users, request):
        parse_date = None
        if request:
            parse_date = request[0]
        start_date = get_valid_date(parse_date)
        response = self.RESPONSE_HEADER + start_date.strftime("%m/%d/%Y")
        iteration = get_iteration_by_date(start_date)
        perform_action = get_action_authorized(self, self.plan)
        stories = None
        if iteration:
            stories = [story for story in get_stories_for_sprint(iteration.oid)]
        if is_authorized_date(start_date) and iteration and stories:
            state = perform_action(iteration, stories)

            response += '\n' + '\n'.join(['Story #' + story.FormattedID + ': '
                                          + story.Name + ' (Proposed Assignee: ' + (str(
                story.Owner.DisplayName) if story.Owner else 'None')
                                          + ' Points = ' + str(story.PlanEstimate) + ')'
                                          for story in stories])
        else:
            response += self.INVALID_RESPONSE
            state = 0
        return response, state
