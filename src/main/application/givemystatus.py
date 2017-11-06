# Use Case: status update

from datetime import datetime

from main.data.commands import GIVEMYSTATUS
from main.service.github import get_commits
# from main.data.validator import get_valid_date


class StatusUpdate:
    def __init__(self):
        self.command = GIVEMYSTATUS
        self.RESPONSE_HEADER = "Here is your status for "
        self.INVALID_RESPONSE = "\nCurrently you have no commits."

    def get_response(self, user, all_users, request, *args, **kwargs):
        parse_date = None
        if request:
            parse_date = request[0]
        # status_date = get_valid_date(parse_date)
        try:
            status_date = datetime.strptime(parse_date, "%m/%d/%Y")
        except Exception as e:
            status_date = datetime.today()
        response = self.RESPONSE_HEADER + status_date.strftime("%m/%d/%Y")

        user_email = None
        for user_obj in all_users:
            if user_obj.slack_id == user:
                user_email = user_obj.email
                user_tz = user_obj.tz
                break

        commits = get_commits(user, user_email, status_date, user_tz)
        if commits:
            response += "\n" + "\n".join([" => ".join(commit) for commit in commits])
        else:
            response += self.INVALID_RESPONSE
        return response

    def give(self):
        pass
