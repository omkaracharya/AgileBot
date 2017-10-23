from main.data.commands import GIVEMYSTATUS, GROOMBACKLOG, PLANSPRINT
from main.data.givemystatus import StatusUpdate
from main.data.groombacklog import GroomBacklog
from main.data.plansprint import PlanSprint

# Singletons
sprint_plan = PlanSprint()
groomed_backlog = GroomBacklog()
status_update = StatusUpdate()

supported_actions = {PLANSPRINT: sprint_plan, GROOMBACKLOG: groomed_backlog, GIVEMYSTATUS: status_update}


def get_action(command):
    return supported_actions[command]


def get_usage():
    return "*Usage:* `plansprint startdate enddate` or `givemystatus statusdate` or `groombacklog`" \
           "\n*Date format:* MM/DD/YYYY"
