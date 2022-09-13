import machine
led = machine.Pin(6, machine.Pin.OUT)
button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    led.value(not button.value())