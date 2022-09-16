from machine import Timer
from components.square_wave import SquareWave


class LED:
    """
    Blinky boy.
    """

    def __init__(self, pin_number, brightness=1, flash_per_sec=0, on=False):
        """
        Create an LED with the given pin number, brightness, flash rate and initial state.
        """
        self._pwm = SquareWave(pin_number=pin_number)
        self._brightness = brightness
        self._timer = Timer(-1)
        if on:
            self.on()
        if flash_per_sec > 0:
            self._flash_per_sec = flash_per_sec
            self._init_timer()

    def _init_timer(self):
        self._timer.init(
            period=round(1000 / self._flash_per_sec),
            mode=Timer.PERIODIC,
            callback=self.toggle,
        )

    def toggle(self, timer=None):
        """
        Change the LED from on to off or vice versa.
        Don't affect blinking
        :param timer:
        :return:
        """
        if self.is_on():
            # TODO: this is no good because we have to disable the timer when we stop, but we don't want to when we blink
            # Solution: remove all timers & duration (except for blink timer) from LED and SquareWave
            # now we can start and stop PWM with correct params
            self.off()
        else:
            self.on()

    def on(self, brightness=None, flash_per_sec=0, duration_sec=0):
        """
        Light up the LED with the given brightness, flash rate and duration.
        :param brightness:
        :param flash_per_sec:
        :param duration_sec:
        :return:
        """
        if brightness is None:
            brightness = self._brightness
        if flash_per_sec > 0:
            self._flash_per_sec = flash_per_sec
            self._init_timer()
        if self._pwm.is_running:
            self._pwm.stop()
        self._pwm.start(frequency=100, duty=brightness, duration_sec=duration_sec)

    def off(self):
        """
        Turn the LED off.
        :return:
        """
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

    def update_duration(self, duration_sec):
        """
        Set the LED timeout to the given duration in seconds.
        """
        self._pwm.start_timer(duration_sec)

    def update_flash_per_sec(self, flash_per_sec):
        """
        Set the LED flash rate to the given number of flashes per second.
        :param flash_per_sec:
        :return:
        """
        self._flash_per_sec = flash_per_sec
        self._init_timer()

    # TODO add fade_on, fade_off, pulse effects
