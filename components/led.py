from machine import Timer
from components.square_wave import SquareWave


class LED:
    """
    Blinky boy.
    """

    # TODO add fade_on, fade_off, pulse effects

    def __init__(self, pin_number, brightness=1, flash_per_sec=0, on=False):
        """
        Create an LED with the given pin number, brightness, flash rate and initial state.
        """
        self._pwm = SquareWave(pin_number=pin_number, frequency=100, duty=brightness, start_active=False)
        self._brightness = brightness
        self._flash_per_sec = flash_per_sec
        self._timer = Timer(-1)
        if on:
            self.on()

    def _init_timer(self):
        if self._flash_per_sec > 0:
            self._timer.init(
                period=round(1000 / self._flash_per_sec),
                mode=Timer.PERIODIC,
                callback=self._blink,
            )
        else:
            self._timer.deinit()

    def _blink(self, timer=None):
        """
        Change the LED from on to off or vice versa.
        """
        if self.is_on():
            self._pwm.stop()
        else:
            self._pwm.start()

    def toggle(self):
        """
        Change the LED from on to off or vice versa.
        :param timer:
        :return:
        """
        if self.is_on():
            self.off()
        else:
            self.on()

    def on(self):
        """
        Light up the LED.
        """
        if not self.is_on():
            self._init_timer()
            self._pwm.start()

    def off(self):
        """
        Turn the LED off.
        :return:
        """
        if self.is_on():
            self._timer.deinit()
            self._pwm.stop()

    def is_on(self):
        """
        True if the LED is currently lit, False otherwise.
        """
        return self._pwm.is_running

    def update_brightness(self, brightness):
        """
        Set the LED brightness to the given level 0-1.
        """
        self._pwm.set_duty(brightness)

    def update_flash_per_sec(self, flash_per_sec):
        """
        Set the LED flash rate to the given number of flashes per second.
        :param flash_per_sec:
        :return:
        """
        self._flash_per_sec = flash_per_sec
        self._init_timer()

    def __del__(self):
        self._timer.deinit()
        self._pwm.stop()
