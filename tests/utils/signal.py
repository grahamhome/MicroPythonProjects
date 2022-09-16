class Signal:
    def __init__(self, value=False):
        self.value = value

    def set_true(self):
        self.value = True

    def set_false(self):
        self.value = False

    def toggle(self):
        self.value = not self.value
