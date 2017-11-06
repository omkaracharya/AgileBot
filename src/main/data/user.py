class User:
    def __init__(self, slack_id, email, tz):
        self.slack_id = slack_id
        self.email = email
        self.tz = tz
        self.rally_id = None

    def get_slack_id(self):
        return self.slack_id

    def get_email(self):
        return self.email

    def get_tz(self):
        return self.tz

    def get_rally_id(self):
        return self.rally_id

    def set_rally_id(self, rally_id):
        self.rally_id = rally_id

