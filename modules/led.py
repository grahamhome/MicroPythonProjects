from machine import Pin, Timer
from utime import sleep_ms
from math import floor

DEFAULT_BLINK_DURATION_SEC = 1
DEFAULT_BLINKS_PER_SEC = 8

class LED:
    
    # TODO add properties for brightness
    
    def __init__(self, pin_number, on=False):
        self._led = Pin(pin_number, Pin.OUT)
        self._timer = Timer(-1)
        self._blinks = 0
        self._blinking = False
        self._blinks_duration_sec = DEFAULT_BLINK_DURATION_SEC
        self._blinks_per_sec = DEFAULT_BLINKS_PER_SEC
        if on:
            self.on()
        else:
            self.off()
    
    def on(self):
        self._stop_blink()
        self._led.value(True)
        self.is_on = True
        
    def off(self):
        self._stop_blink()
        self._led.value(False)
        self.is_on = False
    
    def toggle(self):
        self._led.value(not self._led.value())
        self.is_on = not self.is_on
        
    def blink(self, duration_sec=DEFAULT_BLINK_DURATION_SEC, blinks_per_sec=DEFAULT_BLINKS_PER_SEC):
        if not self._blinking:
            self._blinking = True
            self._blink_duration_sec = duration_sec
            self._blinks_per_sec = blinks_per_sec
            self._timer.init(period=floor(1000/self._blinks_per_sec), mode=Timer.PERIODIC, callback=self._blink)
            
    def _stop_blink(self):
        self._timer.deinit()
        self._blink_duration_sec = DEFAULT_BLINK_DURATION_SEC
        self._blinks_per_sec = DEFAULT_BLINKS_PER_SEC
        self._blinks = 0
        self._blinking = False
        self._led.value(False)
        self.is_on = False
            
    def _blink(self, timer):
        if self._blinks < self._blinks_per_sec*self._blink_duration_sec*2:
            self._blinks += 1
            self.toggle()
        else:
            self._stop_blink()