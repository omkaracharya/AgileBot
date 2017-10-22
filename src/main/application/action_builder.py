from main.data.givemystatus import StatusUpdate

# Singletons
sprint_plan = None
groomed_backlog = None
status_update = StatusUpdate()

supported_actions = {"plansprint": sprint_plan, "groombacklog": groomed_backlog, "givemystatus": status_update}

def get_action(command):
    return supported_actions[command]


def get_usage():
    return "*Usage:* `plansprint startdate enddate` or `givemystatus statusdate` or `groombacklog`" \
           "\n*Date format:* MM/DD/YYYY"
