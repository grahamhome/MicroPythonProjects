from machine import Pin
from utime import sleep_ms
class LED:
    def __init__(self, pin_number, on=False):
        self._led = Pin(pin_number, Pin.OUT)
        if on:
            self.on()
        else:
            self.off()
    
    def on(self):
        self._led.value(True)
        self.is_on = True
        
    def off(self):
        self._led.value(False)
        self.is_on = False
    
    def toggle(self):
        self._led.value(not self._led.value())
        self.is_on = not self.is_on
        
    def blink(self, duration_sec):
        self.on()
        for _ in range(duration_sec*2):
            sleep_ms(500)
            self.toggle()