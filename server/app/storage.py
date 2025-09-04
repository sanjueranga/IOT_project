class Storage:
    def __init__(self):
        self.data = []

    def add_data(self, value):
        self.data.append(value)
        if len(self.data) > 100:  # keep only last 100 readings
            self.data.pop(0)

    def get_all(self):
        return self.data
