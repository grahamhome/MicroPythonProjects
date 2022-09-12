import machine
import utime
from button import Button
led_1 = machine.Pin(0, machine.Pin.OUT)
led_2 = machine.Pin(1, machine.Pin.OUT)
#button_1 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_DOWN)
#button_2 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

freq_c = 262
freq_d = 294
freq_e = 330
freq_f = 350
freq_g = 392
freq_a = 440
freq_b = 494
freq_c2 = 523

frequencies = [freq_c, freq_d, freq_e, freq_f, freq_g, freq_a, freq_b, freq_c2]
freq_index = 0
        

def button_irq_handler(pin):
    buzzer = machine.PWM(machine.Pin(4))
    buzzer.duty_u16(32767) # 50% duty cycle
    buzzer.freq(440)
    utime.sleep_ms(1000)
    buzzer.deinit()

        
    
sensor_1 = Button(3, button_irq_handler, trigger_on_press=False)

while True:
    utime.sleep_ms(10000)
