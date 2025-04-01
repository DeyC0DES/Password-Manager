class CaptureToken:
    def __init__(self):
        super().__init__()

    def capture(self):
        import main

        user_data = main.user_data_storage.get_user_data()
        token = user_data.get('token', 'Empty')
        return token
