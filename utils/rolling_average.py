class RollingAverage:
    def __init__(self, window_size):
        self._values = []
        self._index = 0
        self._size = window_size

    def update_and_retrieve(self, value):
        if len(self._values) > self._index:
            self._values[self._index] = value
        else:
            self._values.append(value)
        self._index = (self._index + 1) % self._size

        for value in self._values:
            if self._values.count(value) >= round(len(self._values) / 2):
                return value
        return sum(self._values) / len(self._values)
