import machine
led_1 = machine.Pin(25, machine.Pin.OUT)
led_2 = machine.Pin(2, machine.Pin.OUT)
button_1 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_2 = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.PWM(machine.Pin(3))
buzzer.duty_u16(32767) # 50% duty cycle
frequency = 1000 # 1 Khz

led_state_1 = False
led_state_2 = False

def button_irq_handler(pin):
    global led_state_1
    global led_state_2
    global frequency
    if pin == button_1:
        led_state_1 = not led_state_1
        if frequency < 2000:
            frequency += 50
    else:
        led_state_2 = not led_state_2
        if frequency > 100:
            frequency -= 50
    
button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)
button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq_handler)

while True:
    led_1.value(led_state_1)
    led_2.value(led_state_2)
    buzzer.freq(frequency)
