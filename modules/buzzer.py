from machine import Pin, PWM
from utime import sleep_ms
class Buzzer:
    # C4-C5
    _frequencies = [262, 294, 330, 350, 392, 440, 494, 523]
    
    def __init__(self, pin_number):
        self._pin = Pin(pin_number, Pin.OUT)
        self.buzzer = None
    
    def start(self, tone_code=0):
        self.stop()
        self.buzzer = PWM(self._pin)
        self.buzzer.duty_u16(32767) # 50% duty cycle
        self.buzzer.freq(self._frequencies[tone_code])
        
    def stop(self):
        if self.buzzer:
            self.buzzer.deinit()
        
    def play(self, duration_ms, tone_code=0):
        self.start()
        sleep_ms(duration_ms)
        self.stop()
        