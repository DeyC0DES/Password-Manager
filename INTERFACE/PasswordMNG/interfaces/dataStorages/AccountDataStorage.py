class AccountDataStorage:
    def __init__(self):
        self.account_data = {}

    def set_account_data(self, name, username, fav, old_password, icon):
        self.account_data = {'name': name, 'username': username, 'fav': fav, 'old_password': old_password, 'icon': icon}

    def get_account_data(self):
        return self.account_data

    def clear(self):
        self.account_data = {}