from traffic_control import Intersection

if __name__ == "__main__":
    Intersection(red_led_pin=2, yellow_led_pin=1, green_led_pin=0, road_sensor_pin=3, crosswalk_sensor_pin=5, buzzer_pin=4, green_led_2_pin=7, yellow_led_2_pin=6).start()
