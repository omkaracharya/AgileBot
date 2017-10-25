from main.data.commands import GIVEMYSTATUS, GROOMBACKLOG, PLANSPRINT
from main.data.givemystatus import StatusUpdate
from main.data.groombacklog import GroomBacklog
from main.data.plansprint import PlanSprint


# Singletons
class ActionBuilder:
    def __init__(self):
        self.sprint_plan = None
        self.groomed_backlog = None
        self.status_update = None

    def build(self):
        self.sprint_plan = PlanSprint()
        self.groomed_backlog = GroomBacklog()
        self.status_update = StatusUpdate()
        return self


def get_supported_actions():
    action_builder = ActionBuilder().build()
    return {PLANSPRINT: action_builder.sprint_plan, GROOMBACKLOG: action_builder.groomed_backlog,
            GIVEMYSTATUS: action_builder.status_update}


def get_action(command):
    return get_supported_actions()[command]


def get_usage():
    return "*Usage:* `plansprint startdate enddate` or `givemystatus statusdate` or `groombacklog`" \
           "\n*Date format:* MM/DD/YYYY"
