from utime import sleep_ms

from components.piezo import Piezo
from components.switch import Switch

PIEZO_PIN = 15
PULL_UP_BUTTON_PIN = 16

YES_RESPONSES = ["y", "yes", "ok", "Y", "YES", "OK", ""]


def test_create_on_and_toggle_single_tone():
    with Piezo(pin_number=PIEZO_PIN, frequency_a=Piezo.notes["C4"], start_active=True) as piezo:
        with Switch(pin_number=PULL_UP_BUTTON_PIN, pull_down=False, close_callback=piezo.toggle):
            assert input("Piezo OK? ") in YES_RESPONSES


def test_create_on_and_toggle_dual_tone():
    with Piezo(
        pin_number=PIEZO_PIN, frequency_a=Piezo.notes["C4"], frequency_b=Piezo.notes["C5"], start_active=True
    ) as piezo:
        with Switch(pin_number=PULL_UP_BUTTON_PIN, pull_down=False, close_callback=piezo.switch_frequencies):
            assert input("Piezo OK? ") in YES_RESPONSES
