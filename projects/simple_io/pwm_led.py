import machine

button_1 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)
led = machine.PWM(machine.Pin(25))
duty = 32767
frequency = 1
brightness_change_mode = False


def button_irq_handler(pin):
    global frequency
    if pin == button_1:
        if not brightness_change_mode:
            if frequency < 20:
                frequency += 1
        else:
            if duty < 62385:
                duty += 3150
    else:
        if not brightness_change_mode:
            if frequency > 0:
                frequency -= 1
        else:
            if duty > 3150:
                duty -= 3150


button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)
button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)

while True:
    led.freq(frequency)
    led.duty_u16(duty)
    brightness_change_mode = button_3.value()
