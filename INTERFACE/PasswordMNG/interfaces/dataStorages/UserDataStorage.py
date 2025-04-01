class UserDataStorage:
    def __init__(self):
        self.user_data = {}

    def set_user_data(self, email, username, token):
        self.user_data = {'email': email, 'username': username, 'token': token}

    def get_user_data(self):
        return self.user_data

    def clear(self):
        self.user_data = {}