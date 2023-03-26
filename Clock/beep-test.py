import time
from machine import Pin, Timer, PWM

timer = Timer()
#speaker = Pin(16, Pin.OUT)

sound_toggle = False

def beeper(timer):
    #speaker.toggle()
    global sound_toggle
    if sound_toggle:
        pwm.freq(1000)
        pwm.duty_u16(1024) # multiples of binary
        sound_toggle = False
    else:
        pwm.deinit()
        sound_toggle = True
    
pwm = PWM(Pin(16))
#pwm.freq(1000)
#pwm.duty_u16(1000)
timer.init(freq=3, mode=Timer.PERIODIC, callback=beeper)