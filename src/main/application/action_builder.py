# Builder Pattern class that builds the corresponding singleton action object based on the specified command.

from main.application.groombacklog import GroomBacklog
from main.application.plansprint import PlanSprint

from main.application.givemystatus import StatusUpdate
from main.data.commands import GIVEMYSTATUS, GROOMBACKLOG, PLANSPRINT

# Singletons
sprint_plan = PlanSprint()
groomed_backlog = GroomBacklog()
status_update = StatusUpdate()

supported_actions = {PLANSPRINT: sprint_plan, GROOMBACKLOG: groomed_backlog,
                     GIVEMYSTATUS: status_update}


def get_usage():
    return "*Usage:* `plansprint startdate` or `givemystatus statusdate` or `groombacklog date`" \
           "\n*Date format:* MM/DD/YYYY"


class ActionBuilder:
    @staticmethod
    def build(command):
        return supported_actions[command]
