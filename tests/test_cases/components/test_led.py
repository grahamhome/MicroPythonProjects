from utime import sleep_ms

from components.led import LED
from components.switch import Switch

LED_PIN = 15
PULL_UP_BUTTON_PIN = 16

YES_RESPONSES = ["y", "yes", "ok", "Y", "YES", "OK", ""]


def test_create_off_turn_on():
    with LED(pin_number=LED_PIN) as led:

        with Switch(pin_number=PULL_UP_BUTTON_PIN, close_callback=led.on, pull_down=False):
            print("Press button to turn steady full bright light on")
            assert input("Light OK? ") in YES_RESPONSES
            # Check for exceptions on repeated calls to on()
            print("Now mash that sucker & ensure light remains on")
            assert input("Light OK? ") in YES_RESPONSES


def test_create_on_turn_off():
    with LED(pin_number=LED_PIN, on=True) as led:

        with Switch(pin_number=PULL_UP_BUTTON_PIN, close_callback=led.off, pull_down=False):
            assert input("Steady full bright light visible? ") in YES_RESPONSES
            print("Press button to turn steady full bright light off")
            assert input("Light OK? ") in YES_RESPONSES
            # Check for exceptions on repeated calls to off()
            print("Now mash that sucker & ensure light remains off")
            assert input("Light OK? ") in YES_RESPONSES


def test_create_off_toggle():
    with LED(pin_number=LED_PIN) as led:

        def function():
            led.toggle()

        with Switch(pin_number=PULL_UP_BUTTON_PIN, close_callback=function, pull_down=False):
            print("Press button to turn steady full bright light on and off")
            assert input("Light OK? ") in YES_RESPONSES


def test_create_on_blinking_brightness_toggle():
    with LED(pin_number=LED_PIN, flash_per_sec=5, brightness=0.5, on=True) as led:

        def function():
            led.toggle()

        with Switch(pin_number=PULL_UP_BUTTON_PIN, close_callback=function, pull_down=False):
            print("Press button to turn blinking half bright light on and off")
            assert input("Light OK? ") in YES_RESPONSES


def test_decrease_blink_rate_increase_brightness_on_off():
    brightness = 0.1
    with LED(pin_number=LED_PIN, brightness=brightness, flash_per_sec=10, on=True) as led:
        assert input("Fast flashing dim light visible? ") in YES_RESPONSES

        print("Watch as brightness increases")
        for _ in range(9):
            sleep_ms(1000)
            brightness += 0.1
            led.update_brightness(brightness=brightness)

        print("Watch as flash rate decreases")
        led.update_flash_per_sec(flash_per_sec=2)

        assert input("Slow flashing bright light visible? ") in YES_RESPONSES

        with Switch(pin_number=PULL_UP_BUTTON_PIN, close_callback=led.off, open_callback=led.on, pull_down=False):
            print("Press button to turn blinking bright light off and release to turn on")
            assert input("Light OK? ") in YES_RESPONSES


def test_increase_brightness_and_blink_rate_while_off():
    with LED(pin_number=LED_PIN, brightness=0.1, flash_per_sec=10, on=True) as led:
        assert input("Fast flashing dim light visible? ") in YES_RESPONSES
        print("Watch as brightness increases and flash rate decreases when light comes back on")
        led.off()
        led.update_brightness(brightness=1)
        led.update_flash_per_sec(flash_per_sec=2)
        sleep_ms(1000)
        led.on()
        assert input("Slow flashing bright light visible? ") in YES_RESPONSES
        with Switch(pin_number=PULL_UP_BUTTON_PIN, close_callback=led.toggle, pull_down=False):
            print("Press button to turn slow blinking bright light off and on")
            assert input("Light OK? ") in YES_RESPONSES


def test_create_lights_sequentially():
    with LED(pin_number=LED_PIN, brightness=0.1, flash_per_sec=10, on=True):
        assert input("Fast flashing dim light visible? ") in YES_RESPONSES
    assert input("Light off? ") in YES_RESPONSES
    with LED(pin_number=LED_PIN, brightness=1, flash_per_sec=2, on=True):
        assert input("Slow flashing bright light visible? ") in YES_RESPONSES


def test_create_lights_simultaneously():
    # Edge case
    with LED(pin_number=LED_PIN, brightness=0.1, flash_per_sec=1, on=True):
        sleep_ms(500)
        with LED(pin_number=LED_PIN, brightness=1, flash_per_sec=1, on=True):
            assert input("Light flashing alternately bright and dim? ") in YES_RESPONSES
