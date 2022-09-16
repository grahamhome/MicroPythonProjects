from machine import Pin, Timer


class Switch:
    CHECK_MS = 5
    PRESS_MS = 10
    RELEASE_MS = 20

    _instances = []
    _all_instance_poller = Timer(-1)

    def __init__(
        self,
        pin_number,
        close_callback=None,
        open_callback=None,
        start_active=False,
        pull_down=True,
    ):
        self._pin = Pin(pin_number, mode=Pin.IN, pull=Pin.PULL_DOWN if pull_down else Pin.PULL_UP)
        self._pull_down = pull_down
        self._debounced_state = pull_down if start_active else not pull_down
        self._counter = 0
        self._close_callback = close_callback or (lambda: ...)
        self._open_callback = open_callback or (lambda: ...)
        Switch._instances.append(self)

    def closed(self):
        return self._debounced_state == self._pull_down

    def _reset_counter(self):
        if self.closed:
            self._counter = Switch.PRESS_MS / Switch.CHECK_MS
        else:
            self._counter = Switch.RELEASE_MS / Switch.CHECK_MS

    def raw_state(self):
        return self._pin.value()

    def _update(self):
        raw_state = self.raw_state()
        if raw_state == self._debounced_state:
            self._reset_counter()
        else:
            self._counter -= 1
            if self._counter == 0:
                self._debounced_state = raw_state
                if self.closed():
                    self._close_callback()
                else:
                    self._open_callback()
                self._reset_counter()

    def __del__(self):
        Switch._instances.remove(self)


def _check_button_pins(timer):
    for button in Switch._instances:
        button._update()


Switch._all_instance_poller.init(mode=Timer.PERIODIC, period=Switch.CHECK_MS, callback=_check_button_pins)
