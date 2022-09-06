from machine import Pin
from utime import sleep_ms

class Button:
    def __init__(self, pin_number, callback=None, pull_down=True, trigger_on_press=True):
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_DOWN if pull_down else Pin.PULL_UP)
        self.callback = callback
        self.trigger_on_press = trigger_on_press
        self.button.irq(trigger=Pin.IRQ_RISING, handler=self.debounce_and_trigger)
                
    def debounce_and_trigger(self, pin):
        """
        Responds to a button press event by ensuring the button remains depressed for 20 ms before triggering callback.
        Optionally waits for button release if self.trigger_on_press is False.
        """
        active = 0
        while self.button.value() and active < 20:
            active += 1
            sleep_ms(1)
        if active == 20:
            if not self.trigger_on_press:
                # Wait for release
                while self.button.value():
                    sleep_ms(1)
            if self.callback:
                self.callback(pin)
