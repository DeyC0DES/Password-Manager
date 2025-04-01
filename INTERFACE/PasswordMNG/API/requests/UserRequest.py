import requests

class UserRequest:
    def __init__(self):
        super().__init__()
        self.url = "http://localhost:8081/passwordManager/api/user"

    def register_request(self, username, email, password, cPassword):
        data = {
            "username": username,
            "email": email,
            "password": password,
            "cPassword": cPassword
        }

        response = requests.post(self.url + "/register", json=data)
        return response

    def login_request(self, email, password):
        data = {
            "item1": email,
            "item2": password
        }

        response = requests.post(self.url + "/login", json=data)
        return response

    def forget_password_request(self, email):

        data = {
            "item1": email,
            "item2": None
        }

        response = requests.post(self.url + "/forget", json=data)
        return response

    def forget_password_verify(self, email, code):

        data = {
            "item1": email,
            "item2": code
        }

        response = requests.post(self.url + "/forget/verification", json=data)
        return response

    def request_code(self, email):
        data = {
            "item1": email,
            "item2": None
        }

        response = requests.post(self.url + "/2steps/sendCodeAgain", json=data)
        return response

    def steps_verify(self, email, code):
        data = {
            "item1": email,
            "item2": code
        }

        response = requests.post(self.url + "/2steps/verification", json=data)
        return response

    def email_verify(self, email, code, new_email, new_username, token):
        data = {
            "email": email,
            "code": code,
            "new_email": new_email,
            "new_username": new_username
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(self.url + "/settings/verification", json=data, headers=headers)
        return response

    def delete_verify(self, email, code, token):
        data = {
            "item1": email,
            "item2": code,
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.delete(self.url + "/delete/verification", json=data, headers=headers)
        return response

    def request_delete_code(self, email, token):
        data = {
            "item1": email,
            "item2": None
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(self.url + "/delete/send-code", json=data, headers=headers)
        return response

    def update_account(self, email, new_name , new_email, token):

        data = {
            "email": email,
            "newUsername": new_name,
            "newEmail": new_email
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.put(self.url + '/update', json=data, headers=headers)
        return response

    def update_password(self, email, new_password, token):

        data = {
            "item1": email,
            "item2": new_password
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.put(self.url + "/update/password", json=data, headers=headers)
        return response
