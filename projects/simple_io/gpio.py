import machine
led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

while True:
    led.value(button.value())