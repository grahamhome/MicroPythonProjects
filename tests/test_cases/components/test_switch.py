from utime import sleep_ms
from components.switch import Switch
from tests.utils import Signal
from machine import Pin

LEFT_SWITCH_PULL_UP_PIN = 15
RIGHT_SWITCH_PULL_DOWN_PIN = 16


def wait_both_opened():
    sleep_ms(500)
    left_pin = Pin(LEFT_SWITCH_PULL_UP_PIN, mode=Pin.IN, pull=Pin.PULL_UP)
    right_pin = Pin(RIGHT_SWITCH_PULL_DOWN_PIN, mode=Pin.IN, pull=Pin.PULL_DOWN)
    if not (left_pin.value() and not right_pin.value()):
        print("Open both switches")
    while not (left_pin.value() and not right_pin.value()):
        sleep_ms(500)


def wait_left_switch_closed():
    sleep_ms(500)
    left_pin = Pin(LEFT_SWITCH_PULL_UP_PIN, mode=Pin.IN, pull=Pin.PULL_UP)
    if left_pin.value():
        print("Close and hold left switch")
    while left_pin.value():
        sleep_ms(500)


def test_open_callbacks_alone():
    wait_both_opened()
    signal_1 = Signal()
    signal_2 = Signal()

    Switch(pin_number=LEFT_SWITCH_PULL_UP_PIN, open_callback=signal_1.toggle, pull_down=False)
    Switch(pin_number=RIGHT_SWITCH_PULL_DOWN_PIN, open_callback=signal_2.toggle, pull_down=True)
    print("Close and open left switch")
    while not signal_1.value:
        sleep_ms(500)
        assert not signal_2.value, "Wrong switch closed or detected"
    assert signal_1.value and not signal_2.value, "Wrong switch closed or detected"
    print("Close and open right switch")
    while not signal_2.value:
        sleep_ms(500)
        assert signal_1.value, "Wrong switch closed or detected"
    assert signal_1.value and signal_2.value, "Wrong switch closed or detected"


def test_close_callbacks_alone():
    wait_both_opened()
    signal_1 = Signal()
    signal_2 = Signal()

    Switch(pin_number=LEFT_SWITCH_PULL_UP_PIN, close_callback=signal_1.toggle, pull_down=False)
    Switch(pin_number=RIGHT_SWITCH_PULL_DOWN_PIN, close_callback=signal_2.toggle, pull_down=True)
    print("Close and open left switch")
    while not signal_1.value:
        sleep_ms(500)
        assert not signal_2.value, "Wrong switch closed or detected"
    assert signal_1.value and not signal_2.value, "Wrong switch closed or detected"
    print("Close and open right switch")
    while not signal_2.value:
        sleep_ms(500)
        assert signal_1.value, "Wrong switch closed or detected"
    assert signal_1.value and signal_2.value, "Wrong switch closed or detected"

def test_close_and_open_callbacks_together():
    wait_both_opened()
    signal_1 = Signal()
    signal_2 = Signal()

    Switch(pin_number=LEFT_SWITCH_PULL_UP_PIN, close_callback=signal_1.set_true, open_callback=signal_1.set_false, pull_down=False)
    Switch(pin_number=RIGHT_SWITCH_PULL_DOWN_PIN, close_callback=signal_2.set_true, open_callback=signal_2.set_false, pull_down=True)
    print("Close and hold left switch")
    while not signal_1.value:
        sleep_ms(500)
        assert not signal_2.value, "Wrong switch closed or detected"
    assert signal_1.value and not signal_2.value, "Wrong switch closed or detected"
    print("While continuing to hold left switch, close and hold right switch")
    while not signal_2.value:
        sleep_ms(500)
        assert signal_1.value, "Wrong switch closed or detected"
    assert signal_1.value and signal_2.value, "Wrong switch closed or detected"


def test_closed_status_without_callbacks():
    wait_both_opened()
    switch_left = Switch(pin_number=LEFT_SWITCH_PULL_UP_PIN, pull_down=False)
    switch_right = Switch(pin_number=RIGHT_SWITCH_PULL_DOWN_PIN, pull_down=True)

    print("Close and hold left switch")
    while not switch_left.closed():
        sleep_ms(500)
        assert not switch_right.closed(), "Wrong switch closed or detected"
    assert switch_left.closed() and not switch_right.closed(), "Wrong switch closed or detected"
    print("While continuing to hold left switch, close and hold right switch")
    while not switch_right.closed():
        sleep_ms(500)
        assert switch_left.closed(), "Wrong switch closed or detected"
    assert switch_left.closed() and switch_right.closed(), "Wrong switch closed or detected"


def test_start_active():
    wait_left_switch_closed()
    signal_1 = Signal()
    Switch(pin_number=LEFT_SWITCH_PULL_UP_PIN, pull_down=False, open_callback=signal_1.set_true, close_callback=signal_1.set_false, start_active=True)
    print("Open left switch")
    while not signal_1.value:
        sleep_ms(500)
    assert signal_1.value, "Open not detected"
    print("Close and hold left switch")
    while signal_1.value:
        sleep_ms(500)
    assert not signal_1.value, "Close not detected"
