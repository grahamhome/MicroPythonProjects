from machine import Pin, PWM, Timer

DEFAULT_DURATION_SEC = 2

class SquareWave:
    
    def __init__(self, pin_number):
        self._pin = Pin(pin_number, Pin.OUT)
        self._pwm = None
        self.is_running = False
        self._timer = Timer(-1)
    
    def start(self, frequency, duration_sec=0, duty=0.5):
        if not self.is_running:
            self._frequency = frequency
            self._duration_sec = duration_sec
            self._duty = duty
            self._generate_wave()
            self.start_timer(duration_sec)

    def _generate_wave(self,):
        self.is_running = True
        self._pwm = PWM(self._pin)
        self.set_duty(self._duty)
        self.set_frequency(self._frequency)

    def _stop_wave(self):
        self._pwm.duty_u16(0)
        self.is_running = False
            
    def set_duty(self, duty):
        self._pwm.duty_u16(round(65535*duty))
        self._duty = duty
        
    def set_frequency(self, frequency):
        self._pwm.freq(frequency)
        self._frequency = frequency
        
    def start_timer(self, duration_sec):
        self.stop_timer()
        if duration_sec > 0:
            self._timer.init(period=duration_sec*1000, mode=Timer.ONE_SHOT, callback=self.stop)
        
    def stop_timer(self):
        self._timer.deinit()
        
    def stop(self, timer=None):
        if self.is_running:
            self._stop_wave()
            self.stop_timer()
            
    def toggle(self):
        if self.is_running:
            self._stop_wave()
        else:
            self._generate_wave()