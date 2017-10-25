# Builder Pattern class that builds the corresponding singleton action object based on the specified command.

from main.data.commands import GIVEMYSTATUS, GROOMBACKLOG, PLANSPRINT
from main.data.givemystatus import StatusUpdate
from main.data.groombacklog import GroomBacklog
from main.data.plansprint import PlanSprint

# Singletons
sprint_plan = PlanSprint()
groomed_backlog = GroomBacklog()
status_update = StatusUpdate()

supported_actions = {PLANSPRINT: sprint_plan, GROOMBACKLOG: groomed_backlog,
                     GIVEMYSTATUS: status_update}


def get_supported_actions():
    return supported_actions.keys()


def get_usage():
    return "*Usage:* `plansprint startdate` or `givemystatus statusdate` or `groombacklog date`" \
           "\n*Date format:* MM/DD/YYYY"


class ActionBuilder:
    @staticmethod
    def build(command):
        return supported_actions[command]
