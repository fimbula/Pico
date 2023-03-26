# Multiple Timer test

import time

from machine import Timer

timer1 = Timer()
timer2 = Timer()

def beeper(timer):
    print("timer1")
    
def oneshot(timer):
    print("one shot")

print("restart")
timer1.init(freq=1, mode=Timer.PERIODIC, callback=beeper)
timer2.init(mode=Timer.ONE_SHOT, period=1000, callback=oneshot)
time.sleep(5)
timer2.init(mode=Timer.ONE_SHOT, period=1000, callback=oneshot)