from machine import Pin
from time import sleep_ms
from utime import sleep_us, ticks_us, ticks_diff

_SPEED_OF_SOUND = 340  # m/s at sea level
TX_DURATION = 10  # microseconds
MEASUREMENT_THRESHOLD = 0.1  # centimeters


class UltrasonicSensor:
    _conversion_rate = (
        _SPEED_OF_SOUND / 10_000 / 2
    )  # Conversion factor from microsecond pulses to distance in centimeters

    def __init__(self, tx_pin_number, rx_pin_number):
        self._tx = Pin(tx_pin_number, Pin.OUT)
        self._rx = Pin(rx_pin_number, Pin.IN)
        self._reset()

    def _reset(self):
        self._rx_start = 0
        self._rx_end = 0

    def _set_rx_start(self):
        self._rx_start = ticks_us()
        self._rx.irq(trigger=Pin.IRQ_FALLING, handler=lambda _s: self._set_rx_end())

    def _set_rx_end(self):
        self._rx_end = ticks_us()

    def distance(self):
        """
        Returns the measured distance in centimeters.
        """
        self._reset()
        self._tx.off()
        self._rx.irq(trigger=Pin.IRQ_RISING, handler=lambda _: self._set_rx_start())
        self._tx.on()
        sleep_us(TX_DURATION)
        self._tx.off()
        while not self._rx_end > self._rx_start:
            sleep_ms(10)
        return ticks_diff(self._rx_end, self._rx_start) * self._conversion_rate
