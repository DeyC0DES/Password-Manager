class InfoDataStorage:
    def __init__(self):
        self.info_data = {}

    def set_info_data(self, message):
        self.info_data = {'content': message}

    def get_info_data(self):
        return self.info_data

    def clear(self):
        self.info_data = {}