from machine import Timer

from components.square_wave import SquareWave


class Piezo:

    notes = {
        "C4": 262,
        "D4": 294,
        "E4": 330,
        "F4": 349,
        "G4": 392,
        "A4": 440,
        "B4": 494,
        "C5": 523,
        "D5": 587,
        "E5": 659,
        "F5": 699,
        "G5": 784,
        "A5": 880,
        "B5": 988,
    }

    def __init__(self, pin_number, frequency_a, frequency_b=None, beep_duration_ms=0, start_active=False):
        self._pwm = SquareWave(pin_number=pin_number, duty=0.5, frequency=frequency_a, start_active=start_active)
        self._frequency_a = frequency_a
        self._frequency_b = frequency_b
        self._freq_a_active = True
        self._beep_duration_ms = beep_duration_ms
        self._timer = Timer(-1)
        if start_active:
            self._init_timer()

    def _init_timer(self):
        if self._beep_duration_ms > 0:
            self._timer.init(
                period=self._beep_duration_ms,
                mode=Timer.PERIODIC,
                callback=self.switch_frequencies,
            )
        else:
            self._timer.deinit()

    def on(self):
        self._pwm.start()
        self._init_timer()

    def off(self):
        self._pwm.stop()
        self._timer.deinit()

    def toggle(self):
        self._pwm.toggle()

    def switch_frequencies(self, timer=None):
        if self._frequency_b:
            if self._freq_a_active:
                self._pwm.set_frequency(self._frequency_b)
            else:
                self._pwm.set_frequency(self._frequency_a)
            self._freq_a_active = not self._freq_a_active
        else:
            self._pwm.stop()

    def delete(self):
        self.__del__()

    def __del__(self):
        self.off()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()
