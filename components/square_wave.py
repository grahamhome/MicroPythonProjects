from machine import Pin, PWM, Timer


class SquareWave:
    """
    A square waveform generator.
    """

    def __init__(self, pin_number, frequency, duty, start_active=True):
        self._pin = Pin(pin_number, Pin.OUT)
        self._frequency = frequency
        self._duty = duty
        self._pwm = None
        self.is_running = False
        if start_active:
            self.start()

    def start(self):
        """
        Start the square wave signal with the given frequency and duty cycle.
        """
        if not self.is_running:
            self._generate_wave()

    def _generate_wave(
        self,
    ):
        """
        Starts the square wave signal.
        """
        self.is_running = True
        self._pwm = PWM(self._pin)
        self.set_duty(self._duty)
        self.set_frequency(self._frequency)

    def _stop_wave(self):
        """
        Terminates the square wave signal.
        :return:
        """
        self._pwm.duty_u16(0)
        self.is_running = False

    def set_duty(self, duty):
        """
        Set the wave duty cycle from 0-1.
        :param duty:
        :return:
        """
        self._pwm.duty_u16(round(65535 * duty))
        self._duty = duty

    def set_frequency(self, frequency):
        """
        Set the wave frequency in Hz.
        :param frequency:
        :return:
        """
        self._pwm.freq(frequency)
        self._frequency = frequency

    def stop(self, timer=None):
        """
        Disable the square wave and end the duration timer.
        :param timer:
        :return:
        """
        self._stop_wave()

    def toggle(self):
        """
        Enable or disable the square wave without affecting the duration timer.
        :return:
        """
        if self.is_running:
            self.stop()
        else:
            self.start()
