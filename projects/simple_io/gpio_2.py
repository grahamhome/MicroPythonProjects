import machine

led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    led.value(not button.value())
