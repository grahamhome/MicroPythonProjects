import machine

led_1 = machine.Pin(25, machine.Pin.OUT)
led_2 = machine.Pin(2, machine.Pin.OUT)
button_1 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_2 = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)


led_state_1 = False
led_state_2 = False


def button_irq_handler(pin):
    global led_state_1
    global led_state_2
    if pin == button_1:
        led_state_1 = not led_state_1
    else:
        led_state_2 = not led_state_2


button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)
button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)

while True:
    led_1.value(led_state_1)
    led_2.value(led_state_2)
