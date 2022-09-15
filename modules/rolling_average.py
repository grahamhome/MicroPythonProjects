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
        return sum(self._values)/len(self._values)