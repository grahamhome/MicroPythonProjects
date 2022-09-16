import machine

led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

led_state = False


def button_irq_handler(pin):
    global led_state
    led_state = not led_state


button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)

while True:
    led.value(led_state)
