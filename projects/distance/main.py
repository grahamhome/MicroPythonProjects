from components.button_old import Button
from components.ultrasonic_sensor import UltrasonicSensor
from components.led import LED
from utime import sleep_ms
from utils.rolling_average import RollingAverage

max_distance = 20
min_distance = 4
max_freq = 2000
min_freq = 100


def main():
    sensor = UltrasonicSensor(1, 0)
    distance = sensor.distance()
    max_dist = 50
    min_dist = 4
    trigger = Button(pin_number=16, callback=lambda _: print(distance), pull_down=False)
    led = LED(pin_number=15)
    led.on(brightness=0.5)
    window = RollingAverage(window_size=50)
    distance = 0
    while 1:
        sleep_ms(100)
        dist = window.update_and_retrieve(sensor.distance())
        if abs(distance - dist) > 0.2:
            distance = dist
            print(dist)
            led.update_flash_per_sec(100 * (dist - min_dist) / (max_dist - min_dist))


if __name__ == "__main__":
    main()
