import time
from machine import Pin

snooze = False
count = 0

button_snooze = Pin(5, Pin.IN, Pin.PULL_UP)

    
def snoozeHandler(pin):
    global snooze, count
    #tim.init(freq = 1, mode=Timer.PERIODIC, callback = buttonTimer)
    pin.irq(handler=None)
    
    #print("snoozehandler")
    count = 0
    
    while pin.value() == 0 and count < 2:
        time.sleep(0.1)
        count += 0.1
    #tim.deinit()
    snooze = True
    pin.irq(handler=snoozeHandler)
    
button_snooze.irq(trigger=Pin.IRQ_FALLING, handler=snoozeHandler)
#tim.init(freq = 1, mode=Timer.PERIODIC, callback = buttonTimer)

while True:
    if snooze:
        print ("snooze pressed")
        #snooze = False
        if count >= 2:
            print ("button pressed for 2")
            count = 0
            #jump to settings
        snooze = False
    time.sleep(0.2)