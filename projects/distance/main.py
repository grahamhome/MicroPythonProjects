from components.ultrasonic_sensor import UltrasonicSensor
from components.led import LED
from utime import sleep_ms
from utils.rolling_average import RollingAverage
from utils.graceful_exit import graceful_exit

max_distance = 20
min_distance = 4
max_freq = 2000
min_freq = 100


@graceful_exit
def main():
    sensor = UltrasonicSensor(1, 0)
    max_dist = 50
    min_dist = 12
    window = RollingAverage(window_size=10)
    distance = 0
    with LED(pin_number=15) as led:
        while 1:
            sleep_ms(500)
            dist = window.update_and_retrieve(round(sensor.distance(), 2))
            if abs(distance - dist) > 0.2:
                distance = dist
                print(dist)
                led.update_flash_per_sec(30 * (dist - min_dist) / (max_dist - min_dist))
