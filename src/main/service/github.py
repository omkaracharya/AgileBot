from main.application.authority import Authority


def get_commits(user, date):
    if not Authority.is_authorized_date(date):
        return None
    # TODO: Implement service/ mock file
    return "\nSome commit message for some commit id."
