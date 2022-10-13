from components.switch import Switch
from machine import Pin


class Multiplexer:
    """
    Designed for use with multiplexer circuits with a horizontal column of input pins
    and a vertical row of output pins.
    """

    def __init__(
        self,
        input_pin_numbers,
        output_pin_numbers,
        key_symbols_ltr,
        on_close_callback=lambda _: ...,
        on_open_callback=lambda _: ...,
    ):
        # Will not attempt to initialize with illegal values
        assert isinstance(input_pin_numbers, list) and all(
            isinstance(n, int) for n in input_pin_numbers
        ), "First argument must be a list of input pin numbers in top-down order"
        assert isinstance(output_pin_numbers, list) and all(
            isinstance(n, int) for n in output_pin_numbers
        ), "Second argument must be list of output pin numbers from left-to-right order"
        assert isinstance(key_symbols_ltr, list) and all(
            isinstance(n, str) and len(n) == 1 for n in key_symbols_ltr
        ), "Third argument must be list of single chars representing key symbols from left-to-right and top-down"
        assert len(key_symbols_ltr) == len(input_pin_numbers) * len(
            output_pin_numbers
        ), "Incorrect number of key symbols in third argument"

        self._on_open_callback = on_open_callback
        self._on_close_callback = on_close_callback
        self._output_pins = {
            pin_id: Pin(pin_number, mode=Pin.OUT)
            for pin_number, pin_id in zip(output_pin_numbers, range(3, (len(output_pin_numbers) + 2) * 2, 2))
        }
        self._output_pin_index = len(self._output_pins) - 1
        self._switches = {
            switch_id: Switch(
                pin_number=pin_number,
                close_callback=lambda: self._handle_trigger(switch_id, closed=True),
                open_callback=lambda: self._handle_trigger(switch_id, closed=False),
            )
            for pin_number, switch_id in zip(input_pin_numbers, range(2, (len(input_pin_numbers) + 1) * 2, 2))
        }
        self._symbol_map = {
            virtual_switch_id: symbol
            for virtual_switch_id, symbol in zip(
                [
                    output_pin_id * switch_id
                    for switch_id in sorted(self._switches.keys())
                    for output_pin_id in sorted(self._output_pins.keys())
                ],
                key_symbols_ltr,
            )
        }

    def _increment_pin_index(self):
        self._output_pin_index = (self._output_pin_index + 1) % len(self._output_pins)

    def _get_active_pin_id(self):
        return sorted(self._output_pins.keys())[self._output_pin_index]

    def _handle_trigger(self, switch_id, closed):
        """
        Calls the provided callback method, passing the symbol
        associated with the key that was closed or opened.
        """
        if closed:
            self._on_close_callback(self._symbol_map[switch_id * self._get_active_pin_id()])
        else:
            self._on_open_callback(self._symbol_map[switch_id * self._get_active_pin_id()])

    def update(self):
        """
        Sets the active pin to low, updates the active pin index and sets the new active pin to high.
        """
        self._output_pins[self._get_active_pin_id()].off()
        self._increment_pin_index()
        self._output_pins[self._get_active_pin_id()].on()
