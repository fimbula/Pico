import time
from machine import Pin, I2C

button_snooze = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
button_menu = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
button_plus = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_minus = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

menu = False
plus = False
minus = False
snooze = False

def menuHandler(pin):
    global menu
    pin.irq(handler=None)
    menu = True
    while pin.value == 0:
        time.sleep(0.1)
    time.sleep(0.5)
    pin.irq(handler=menuHandler)
    
def snoozeHandler(pin):
    global snooze
    pin.irq(handler=None)
    snooze = True
    while pin.value == 0:
        time.sleep(0.1)
    time.sleep(0.5)
    pin.irq(handler=snoozeHandler)
    
def plusHandler(pin):
    global plus
    pin.irq(handler=None)
    plus = True
    while pin.value == 0:
        time.sleep(0.1)
    time.sleep(0.5)
    pin.irq(handler=plusHandler)
    
def minusHandler(pin):
    global minus
    pin.irq(handler=None)
    minus = True
    while pin.value == 0:
        time.sleep(0.1)
    time.sleep(0.5)
    pin.irq(handler=minusHandler)
    
def settings():
    global snooze, plus, minus, menu
    menu = False
    print("Alarm")
    start_time = time.time()
    while (time.time() - start_time) < 5:
        if snooze:
            snooze = False
            break
        if plus:
            plus = False
            print("adding")
            start_time = time.time()
        if minus:
            minus = False
            print("subtract")
            start_time = time.time()
        if menu:
            menu = False
            print("moving cursor right")
            start_time = time.time()
        time.sleep(0.1)
    
    print("Year")

    return
    
button_menu.irq(trigger=machine.Pin.IRQ_FALLING, handler=menuHandler)
button_plus.irq(trigger=machine.Pin.IRQ_FALLING, handler=plusHandler)
button_minus.irq(trigger=machine.Pin.IRQ_FALLING, handler=minusHandler)
button_snooze.irq(trigger=machine.Pin.IRQ_FALLING, handler=snoozeHandler)

while True:
    if menu:
        print("selecting menu")
        menu = False
        settings()
    time.sleep(0.1)