from modules.button import Button
from modules.ultrasonic_sensor import UltrasonicSensor
from modules.led import LED
from utime import sleep_ms

max_distance = 20
min_distance = 4
max_freq = 2000
min_freq = 100

def main():
    # sensor = UltrasonicSensor(1, 0)
    distance = 0
    trigger = Button(pin_number=16, callback=lambda _: print(distance), pull_down=False)
    led = LED(pin_number=15)
    brightness = 1
    led.on(brightness=brightness, duration_sec=1)
    while brightness > 0:
        sleep_ms(1000)
        brightness -= 0.1
        led.update_brightness(brightness)
        