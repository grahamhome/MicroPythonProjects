from machine import Pin, PWM, Timer


class SquareWave:
    """
    A square waveform generator.
    """

    def __init__(self, pin_number, frequency, duty, start_active=True):
        self._pin = Pin(pin_number, Pin.OUT)
        self._frequency = frequency
        self._duty = duty
        self._pwm = PWM(self._pin)
        self.is_running = False
        if start_active:
            self.start()
        else:
            self.stop()

    def start(
        self,
    ):
        """
        Starts the square wave signal.
        """
        self.set_duty(self._duty)
        self.set_frequency(self._frequency)
        self.is_running = True

    def stop(self):
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

    def toggle(self, timer=None):
        """
        Enable or disable the square wave.
        :return:
        """
        if self.is_running:
            self.stop()
        else:
            self.start()
