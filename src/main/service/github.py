# Service that interacts with GitHub.

from main.application.authority import is_authorized_date


def get_commits(user, date):
    if not is_authorized_date(date):
        return None
    # TODO: Implement service/ mock file
    return "\nSome commit message for some commit id."
