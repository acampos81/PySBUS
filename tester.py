import time

class TestClass():
    def __init__(self):
        self._timer = 0
        self._payload = [0] * 3
        self._current_timeout = 0
        self._current_milli_time = lambda: int(round(time.time() * 1000))
        self._last_milli_time = 0

    def payload(self):
        payload = self._payload
        payload[0] = 1
        payload[1] = 2
        payload[2] = 3
        print(self._payload)

    def timer(self):
        t = self._timer
        t = 3
        print(self._timer)

    def if_bytes(self, b1, b2):
        if (b1 & b2) or\
                (b1 | b2) == 0x03:
            print("yes")

    def time_delta(self):
        if self._last_milli_time == 0:
            self._last_milli_time = self._current_milli_time()
        else:
            self._current_timeout = self._current_milli_time() - self._last_milli_time
            self._last_milli_time = self._current_milli_time()

        print(self._current_timeout)
