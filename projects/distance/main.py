from modules.button import Button
from modules.ultrasonic_sensor import UltrasonicSensor
from utime import sleep_ms

if __name__ == "__main__":
    sensor = UltrasonicSensor(1, 0)
    distance = 0
    trigger = Button(pin_number=16, callback=lambda _: print(distance))
    while 1:
        sleep_ms(100)
        distance = f"{sensor.distance()*0.393701} in"