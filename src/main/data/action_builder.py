supported_actions = {"plansprint": None, "groombacklog": None, "givemystatus": None}


def get_action(command):
    return supported_actions[command]


def get_usage():
    return "*Usage:* `plansprint startdate enddate` or `givemystatus statusdate` or `groombacklog`" \
           "\n*Date format:* MM/DD/YYYY"
