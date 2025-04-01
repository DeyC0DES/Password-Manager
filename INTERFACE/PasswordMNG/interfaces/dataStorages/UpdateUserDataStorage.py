class UpdateUserDataStorage:
    def __init__(self):
        self.account_data = {}

    def set_update_data(self, email, new_username, new_email):
        self.account_data = {'email': email, 'new_username': new_username, 'new_email': new_email}

    def get_update_data(self):
        return self.account_data

    def clear(self):
        self.account_data = {}