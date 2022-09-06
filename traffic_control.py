from modules.button import Button
from modules.led import LED
from modules.buzzer import Buzzer
from _thread import start_new_thread
from utime import sleep_ms
from machine import Timer
    
class PeopleMover:
    def __init__(self, stop_delay_sec, start_delay_sec, moving=False):
        self._moving = moving
        self.should_move = moving
        self._stop_delay_sec = stop_delay_sec
        self._start_delay_sec = start_delay_sec
        if self._moving:
            self._go()
        else:
            self._stop()
        
    def run(self):
        while 1:
            if self._moving != self.should_move:
                if self._moving:
                    self._moving = self.should_move
                    self._slow_and_stop()
                else:
                    self._moving = self.should_move
                    Timer(-1).init(period=self._start_delay_sec*1000, mode=Timer.ONE_SHOT, callback=self._go)
                
            sleep_ms(500)
            
    def _stop(self, _=None):
        self._moving = False
        
    def _go(self, _=None):
        self._moving = True
        
    def _slow_and_stop(self):
        self._moving = True
        Timer(-1).init(period=self._stop_delay_sec*1000, mode=Timer.ONE_SHOT, callback=self._stop)
    
    

class TrafficLight(PeopleMover):
    def __init__(self, red_led_pin, yellow_led_pin, green_led_pin, stop_delay_sec, start_delay_sec, moving):
        self._red = LED(red_led_pin)
        self._yellow = LED(yellow_led_pin)
        self._green = LED(green_led_pin)
        super().__init__(stop_delay_sec, start_delay_sec, moving)
    
    def _red_light(self):
        self._red.on()
        self._yellow.off()
        self._green.off()
    
    def _yellow_light(self):
        self._red.off()
        self._yellow.on()
        self._green.off()
        
    def _green_light(self):
        self._red.off()
        self._yellow.off()
        self._green.on()
    
    def _go(self, _=None):
        self._green_light()
        super()._go()
        
    def _stop(self, _=None):
        self._red_light()
        super()._stop()
        
    def _slow_and_stop(self):
        self._yellow_light()
        super()._slow_and_stop()
            
class CrosswalkLight(PeopleMover):
    def __init__(self, green_led_pin, yellow_led_pin, buzzer_pin, stop_delay_sec, start_delay_sec, moving):
        self._green = LED(green_led_pin)
        self._yellow = LED(yellow_led_pin)
        self._buzzer = Buzzer(buzzer_pin)
        super().__init__(stop_delay_sec, start_delay_sec, moving)
        
    def _green_light(self):
        self._green.on()
        self._yellow.off()
        
    def _yellow_light(self):
        self._green.off()
        self._yellow.on()
        
    def _slow_and_stop(self):
        self._yellow_light()
        self._buzzer.start(tone_code=6, duration_sec=self._stop_delay_sec)
        self._yellow.blink(self._stop_delay_sec)
        super()._slow_and_stop()
        
    def _go(self, _=None):
        self._green_light()
        self._buzzer.start(tone_code=7, duration_sec=1)
        super()._go()
    
    def _stop(self, _=None):
        self._yellow_light()
        super()._stop()
        

class Intersection:
    def __init__(self, red_led_pin, yellow_led_pin, green_led_pin, road_sensor_pin, crosswalk_sensor_pin, buzzer_pin, green_led_2_pin, yellow_led_2_pin):
        crosswalk_yellow_duration_sec = 2
        traffic_yellow_duration_sec = 5
        self._traffic_light = TrafficLight(red_led_pin, yellow_led_pin, green_led_pin, traffic_yellow_duration_sec, crosswalk_yellow_duration_sec, moving=False)
        self._cars_waiting = 0
        self._crosswalk_light = CrosswalkLight(green_led_2_pin, yellow_led_2_pin, buzzer_pin, crosswalk_yellow_duration_sec, traffic_yellow_duration_sec, moving=True)
        self._pedestrians_waiting = 0
        self._road_sensor = Button(road_sensor_pin, callback=self._car_arrives)
        self._crosswalk_sensor = Button(crosswalk_sensor_pin, callback=self._pedestrian_arrives, pull_down=False)
        
    def _car_arrives(self, _):
        self._cars_waiting += 1
        self._traffic_light.should_move = self._cars_waiting >= self._pedestrians_waiting
        self._crosswalk_light.should_move = not self._traffic_light.should_move
        
    def _pedestrian_arrives(self, _):
        self._pedestrians_waiting += 1
        self._traffic_light.should_move = self._cars_waiting >= self._pedestrians_waiting
        self._crosswalk_light.should_move = not self._traffic_light.should_move
        
    def start(self):
        start_new_thread(self._traffic_light.run, ())
        self._crosswalk_light.run()

if __name__ == "__main__":
    Intersection(red_led_pin=2, yellow_led_pin=1, green_led_pin=0, road_sensor_pin=3, crosswalk_sensor_pin=5, buzzer_pin=4, green_led_2_pin=7, yellow_led_2_pin=6).start()

