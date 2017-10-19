class Bot:
    def __init__(self, id, token, name="agilebot"):
        self.id = id
        self.token = token
        self.name = name
        self.address = self.get_address()

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_name(self):
        return self.name

    def set_name(self, name="agilebot"):
        self.name = name

    def get_address(self):
        return "<@" + self.get_id() + ">"
