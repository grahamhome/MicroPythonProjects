from machine import Pin, PWM, Timer

DEFAULT_DURATION_SEC = 2

class Buzzer:
    # C4-C5
    _frequencies = [262, 294, 330, 350, 392, 440, 494, 523]
    
    def __init__(self, pin_number):
        self._pin = Pin(pin_number, Pin.OUT)
        self._buzzer = None
        self._is_buzzing = False
    
    def start(self, tone_code=0, duration_sec=DEFAULT_DURATION_SEC):
        if not self._is_buzzing:
            self._is_buzzing = True
            self._buzzer = PWM(self._pin)
            self._buzzer.duty_u16(32767) # 50% duty cycle
            self._buzzer.freq(self._frequencies[tone_code])
            Timer(-1).init(period=duration_sec*1000, mode=Timer.ONE_SHOT, callback=self.stop)
        
        
    def stop(self, timer=None):
        if self._is_buzzing:
            self._buzzer.deinit()
            self._is_buzzing = False
        