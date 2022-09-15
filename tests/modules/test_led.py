from modules.led import LED
from modules.button import Button

LED_PIN = 15
PULL_UP_BUTTON_PIN = 16

YES_RESPONSES = ["y", "yes", "ok", "Y", "YES", "OK"]


def test_create_off_turn_on():
    led = LED(pin_number=LED_PIN)

    def test(pin):
        led.on()

    button = Button(pin_number=PULL_UP_BUTTON_PIN, callback=test, pull_down=False)
    print("Press button to turn steady full bright light on")
    assert input("Light OK? ") in YES_RESPONSES
    # Check for exceptions on repeated calls to on()
    print("Now mash that sucker")
    assert input("Light OK? ") in YES_RESPONSES


def test_create_on_turn_off():
    led = LED(pin_number=LED_PIN, on=True)

    def test(pin):
        led.off()

    button = Button(pin_number=PULL_UP_BUTTON_PIN, callback=test, pull_down=False)
    assert input("Steady full bright light visible? ") in YES_RESPONSES
    print("Press button to turn steady full bright light off")
    assert input("Light OK? ") in YES_RESPONSES
    # Check for exceptions on repeated calls to off()
    print("Now mash that sucker")
    assert input("Light OK? ") in YES_RESPONSES

def test_create_on_blinking():
    ...

def test_create_on_brightness():
    ...

def test_toggle_on_off():
    ...

def test_toggle_on_off_blinking():
    ...

def test_toggle_on_off_timed():
    ...

def test_toggle_on_off_timed_blinking():
    ...

def test_increase_decrease_blink_rate():
    ...

def test_increase_decrease_timeout():
    ...

def test_increase_decrease_brightness():
    ...