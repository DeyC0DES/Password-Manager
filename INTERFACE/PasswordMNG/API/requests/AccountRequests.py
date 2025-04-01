import requests

class AccountRequests:
    def __init__(self):
        super().__init__()
        self.url = "http://localhost:8081/passwordManager/api/account"

    def create_account(self, name, username, password, icon, fav, token):
        data = {
            "name": name,
            "username": username,
            "password": password,
            "icon": icon,
            "fav": fav
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(self.url + '/create', json=data, headers=headers)
        return response

    def get_accounts(self, token):
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(self.url + '/getAccounts', headers=headers)
        return response

    def decode_password(self, name, token):
        data = {
            "item1": name,
            "item2": None
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(self.url + '/decode/password', json=data, headers=headers)
        return response

    def update_account(self, name, newName, newUsername, newPassword, icon, fav, token):
        data = {
            "accountName": name,
            "newUsername": newUsername,
            "newName": newName,
            "newPassword": newPassword,
            "icon": icon,
            "favorite": fav
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.put(self.url + '/update', json=data, headers=headers)
        return response

    def update_fav_account(self, username, fav, token):
        data = {
            "name": username,
            "fav": fav
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.put(self.url + '/update/fav', json=data, headers=headers)
        return response

    def delete_account(self, name, token):
        data = {
            "item1": name,
            "item2": None
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.delete(self.url + '/delete', json=data, headers=headers)
        return response