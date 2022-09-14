from machine import Pin, Timer
from modules.square_wave import SquareWave

class LED:
    
    def __init__(self, pin_number, brightness=1, flash_per_sec=0, on=False):
        self._pwm = SquareWave(pin_number=pin_number)
        self._brightness = brightness
        self._timer = Timer(-1)
        if on:
            self.on()
        else:
            self.off()
        if flash_per_sec > 0:
            self._flash_per_sec = flash_per_sec
            self._init_timer()

    def _init_timer(self):
        self._timer.init(period=round(1000/self._flash_per_sec), mode=Timer.PERIODIC, callback=self.toggle)

    def toggle(self, timer=None):
        self._pwm.toggle()
    
    def on(self, brightness=None, flash_per_sec=0, duration_sec=0):
        if brightness is None:
            brightness = self._brightness
        if flash_per_sec > 0:
            self._flash_per_sec = flash_per_sec
            self._init_timer()
        if self._pwm.is_running:
            self._pwm.stop()
        self._pwm.start(frequency=100, duty=brightness, duration_sec=duration_sec)
        
    def off(self):
        self._pwm.stop()
        
    def is_on(self):
        return self._pwm.is_running
    
    def update_brightness(self, brightness):
        self._pwm.set_duty(brightness)
    
    def update_duration(self, duration_sec):
        self._pwm.set_timer(duration_sec)
