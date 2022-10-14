from components import Multiplexer, Switch, LED
from utime import sleep_ms

current_value = None


def callback(value):
    global current_value
    current_value = value


def main():
    multiplexer = Multiplexer(
        input_pin_numbers=[0, 1],
        output_pin_numbers=[2, 3],
        key_symbols_ltr=["a", "b", "c", "d"],
        on_close_callback=callback,
    )
    print(multiplexer._symbol_map)
    print(multiplexer._switches)
    print(multiplexer._output_pins)
    global current_value
    # while 1:
    #     if current_value:
    #         print(current_value)
    #         current_value = None
    #         sleep_ms(500)

    with LED(pin_number=25) as work_light:
        with Switch(pin_number=15, pull_down=False, close_callback=work_light.toggle) as switchy:
            while 1:
                ...
