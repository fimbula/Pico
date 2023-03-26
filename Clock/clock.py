# Alarm clock 
import time
import framebuf
import rv3028_rtc
from machine import Pin, I2C, PWM, Timer
from ssd1306 import SSD1306_I2C

pwm = PWM(Pin(16))
button_snooze = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
button_alarm = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
button_plus = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_minus = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

alarm_time = "1400"
#date_time = (2020, 1, 15, 0, 10, 32, 36, 0) #(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
plus_pressed = False
alarm_pressed = False
minus_pressed = False
snooze_pressed = False

alarm_set = False
alarm_flag = False
alarm_sounding = False
sound_toggle = False
snooze_enabled = False

WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
timer = Timer()
rtc = rv3028_rtc.RV3028(0x52, i2c, "LSM")
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, 0x3D, reset = 7)

# - - display images - - #
b_one = bytearray(b'\x00\x00\x00\x00\xff\xc0\x00\xff\xc0\x01\xff\xc0\x01\xff\xc0\x03\xff\xc0\x07\xff\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x0f\xc0\x00\x00\x00')
one = framebuf.FrameBuffer(b_one, 24,36, framebuf.MONO_HLSB)
b_two = bytearray(b'\x00\x7f\x00\x01\xff\xc0\x07\xff\xe0\x0f\xff\xf0\x1f\xff\xf8\x1f\xff\xfc?\xc3\xfc?\x80\xfe\x7f\x00\xfc\x7f\x00\xfe~\x00~~\x00\xfe\x00\x00\xfc\x00\x00\xfc\x00\x00\xfc\x00\x01\xfc\x00\x03\xf8\x00\x03\xf0\x00\x07\xf0\x00\x0f\xe0\x00\x1f\xe0\x00?\xc0\x00\x7f\x80\x00\xff\x00\x01\xfe\x00\x03\xfc\x00\x07\xf8\x00\x0f\xf8\x00\x1f\xe0\x00?\xff\xfe\x7f\xff\xfe\xff\xff\xfe\xff\xff\xfe\xff\xff\xfe\xff\xff\xfe\x00\x00\x00')
two = framebuf.FrameBuffer(b_two, 24,36, framebuf.MONO_HLSB)
b_three = bytearray(b'\x00~\x00\x01\xff\xc0\x07\xff\xe0\x0f\xff\xf0\x0f\xff\xf8\x1f\xff\xf8\x1f\xc3\xfc?\x80\xfc?\x00\xfc\x00\x00\xfc\x00\x01\xfc\x00\x03\xf8\x00\x0f\xf8\x00\x7f\xf0\x00\x7f\xe0\x00\x7f\x80\x00\x7f\xe0\x00\x7f\xf8\x00\x7f\xf8\x00\x07\xfc\x00\x01\xfe\x00\x00\xfe\x00\x00~\x00\x00\x7f\x00\x00>\xfe\x00\x7f~\x00~\x7f\x00~\x7f\x00\xfe\x7f\xc3\xfc?\xff\xfc\x1f\xff\xf8\x1f\xff\xf0\x07\xff\xe0\x03\xff\xc0\x00\xfe\x00')
three = framebuf.FrameBuffer(b_three, 24,36, framebuf.MONO_HLSB)
b_four = bytearray(b'\x00\x03\xf8\x00\x07\xf8\x00\x07\xf8\x00\x0f\xf8\x00\x1f\xf8\x00\x1f\xf8\x00?\xf8\x00\x7f\xf8\x00\x7f\xf8\x00\xff\xf8\x01\xff\xf8\x01\xfd\xf8\x03\xfb\xf8\x03\xf1\xf8\x07\xf3\xf8\x0f\xe1\xf8\x0f\xc3\xf8\x1f\xc1\xf8?\x83\xf8?\x03\xf8\x7f\x01\xf8\xfe\x03\xf8\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x03\xf8\x00\x01\xf8\x00\x03\xf8\x00\x01\xf8\x00\x03\xf8\x00\x01\xf8\x00\x03\xf8\x00\x00\x00')
four = framebuf.FrameBuffer(b_four, 24,36, framebuf.MONO_HLSB)
b_five = bytearray(b'\x00\x00\x00\x00\xff\xfe\x01\xff\xfe\x01\xff\xfe\x01\xff\xfe\x01\xff\xfe\x03\xff\xfe\x01\xf0\x00\x03\xf0\x00\x03\xf0\x00\x03\xf0\x00\x07\xe0\x00\x07\xe0\x00\x07\xff\x00\x07\xff\xe0\x07\xff\xf0\x0f\xff\xf8\x0f\xff\xfc\x0f\xff\xfc\x0f\xc1\xfe\x03\x80\xfe\x00\x00~\x00\x00~\x00\x00~\x00\x00>\x00\x00~\x00\x00~\x7f\x00~\x7f\x80\xfe?\xc3\xfe\x1f\xff\xfc\x1f\xff\xf8\x0f\xff\xf0\x07\xff\xe0\x03\xff\xc0\x00~\x00')
five = framebuf.FrameBuffer(b_five, 24,36, framebuf.MONO_HLSB)
b_six = bytearray(b'\x00\x08\x00\x00\x0f\x00\x00\x1f\x80\x00\x1f\xc0\x00?\x80\x00?\x00\x00\x7f\x00\x00~\x00\x00\xfe\x00\x00\xfc\x00\x01\xfc\x00\x01\xfc\x00\x03\xf8\x00\x03\xf0\x00\x07\xfe\x00\x0f\xff\xc0\x0f\xff\xe0\x0f\xff\xf0\x1f\xff\xf0\x1f\xff\xf8?\xc3\xfc?\x81\xfc?\x00\xfc\x7f\x00\xfc~\x00\xfc?\x00\xfc~\x00\xfc?\x01\xfc?\x81\xfc?\xc7\xf8\x1f\xff\xf8\x1f\xff\xf0\x0f\xff\xe0\x07\xff\xc0\x01\xff\x80\x00~\x00')
six = framebuf.FrameBuffer(b_six, 24,36, framebuf.MONO_HLSB)
b_seven = bytearray(b'\x00\x00\x00?\xff\xff?\xff\xff?\xff\xfe?\xff\xff?\xff\xfe?\xff\xfe\x00\x01\xfc\x00\x01\xfc\x00\x03\xf8\x00\x03\xf8\x00\x03\xf0\x00\x07\xf0\x00\x07\xe0\x00\x0f\xe0\x00\x1f\xc0\x00\x1f\xc0\x00\x1f\x80\x00?\x80\x00?\x00\x00\x7f\x00\x00~\x00\x00\xfe\x00\x00\xfc\x00\x01\xfc\x00\x01\xfc\x00\x03\xf8\x00\x03\xf8\x00\x07\xf0\x00\x07\xf0\x00\x0f\xe0\x00\x0f\xe0\x00\x1f\xc0\x00\x1f\xc0\x00\x1f\x80\x00\x00\x00\x00')
seven = framebuf.FrameBuffer(b_seven, 24,36, framebuf.MONO_HLSB)
b_eight = bytearray(b'\x00~\x00\x03\xff\xc0\x07\xff\xe0\x0f\xff\xf0\x1f\xff\xf8\x1f\xff\xf8?\xc3\xf8?\x81\xfc?\x00\xfc?\x00\xfc?\x00\xfc?\x81\xfc\x1f\x81\xfc\x1f\xc3\xf8\x1f\xff\xf0\x0f\xff\xf0\x07\xff\xe0\x0f\xff\xf0\x1f\xff\xf8?\xff\xfc?\x81\xfe\x7f\x00\xfe~\x00~~\x00~\xfe\x00\x7f|\x00>\xfe\x00\x7f~\x00~\x7f\x00\xfe\x7f\xc3\xfe?\xff\xfc?\xff\xfc\x1f\xff\xf8\x0f\xff\xf0\x07\xff\xe0\x00\xff\x00')
eight = framebuf.FrameBuffer(b_eight, 24,36, framebuf.MONO_HLSB)
b_nine = bytearray(b'\x00~\x00\x01\xff\xc0\x03\xff\xe0\x0f\xff\xf0\x0f\xff\xf8\x1f\xff\xf8\x1f\xc3\xfc?\x81\xfc?\x80\xfe?\x00\xfc?\x00~?\x00\xfe?\x00|?\x80\xfe?\x81\xfc\x1f\xc3\xfc\x1f\xff\xf8\x0f\xff\xf8\x0f\xff\xf0\x03\xff\xf0\x01\xff\xe0\x00\x7f\xe0\x00\x0f\xc0\x00\x1f\xc0\x00?\x80\x00?\x80\x00?\x00\x00\x7f\x00\x00\xfe\x00\x00\xfe\x00\x01\xfc\x00\x01\xfc\x00\x03\xf8\x00\x03\xf8\x00\x03\xf0\x00\x00\x00\x00')
nine = framebuf.FrameBuffer(b_nine, 24,36, framebuf.MONO_HLSB)
b_zero = bytearray(b'\x00~\x00\x03\xff\xc0\x07\xff\xe0\x0f\xff\xf0\x1f\xff\xf8\x1f\xff\xf8?\xc3\xfc?\x81\xfc?\x00\xfc~\x00\xfe~\x00~~\x00~~\x00~~\x00~~\x00~~\x00~|\x00>~\x00~~\x00~|\x00>~\x00~~\x00~~\x00~~\x00~~\x00~~\x00\xfe\x7f\x00\xfe?\x00\xfc?\x81\xfc?\xc3\xfc\x1f\xff\xf8\x1f\xff\xf8\x0f\xff\xf0\x07\xff\xe0\x01\xff\xc0\x00~\x00')
zero = framebuf.FrameBuffer(b_zero, 24,36, framebuf.MONO_HLSB)
b_bell = bytearray(b'\x0c\x00\x1e\x00?\x00?\x00\x7f\x80\x7f\x80\xff\xc0\xff\xc0\xff\xc0\x0c\x00')
bell = framebuf.FrameBuffer(b_bell, 10,10, framebuf.MONO_HLSB)
listy = (zero,one,two,three,four,five,six,seven,eight,nine)

def alarmHandler(pin):
    global alarm_pressed, count
    pin.irq(handler=None)
    count = 0
    while pin.value() == 0 and count < 2:
        time.sleep(0.1)
        count += 0.1
    alarm_pressed = True
    pin.irq(handler=alarmHandler)
    
def snoozeHandler(pin):
    global snooze_pressed, count
    pin.irq(handler=None)
    snooze_pressed = True
    while pin.value() == 0:
        time.sleep(0.1)
    pin.irq(handler=snoozeHandler)
    
def plusHandler(pin):
    global plus_pressed
    pin.irq(handler=None)
    plus_pressed = True
    while pin.value() == 0:
        time.sleep(0.1)
    pin.irq(handler=plusHandler)
    
def minusHandler(pin):
    global minus_pressed
    pin.irq(handler=None)
    minus_pressed = True
    while pin.value() == 0:
        time.sleep(0.1)
    pin.irq(handler=minusHandler)

def padTime(digit):
    if len(digit) == 1:
        digit = "0" + digit
    return digit

def isDst():
    month = rtc.get_month()
    day = rtc.get_date()
    weekday =rtc.get_weekday()
    hours = rtc.get_hours()
    if month < 3 and month > 10:
        return False
    if month > 3 and month < 10:
        return True
    if month == 3:
        if day >=25 and (weekday-(day-24))<0:
            return True
        else:
            if weekday == 7 and hour >= 1:
                return True
            else:
                return False
    if month == 10:
        if day >=25 and (weekday-(day-24))<0:
            return False
        else:
            if weekday == 7 and hour >= 2:
                return False
            else:
                return True

def getHours():
    hours = rtc.get_hours()
    if isDst():
        return hours + 1
    else:
        return hours

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

def checkAlarm():
    global alarm_flag, alarm_time, alarm_sounding
    #use an alarm has triggered flag, reset at midnight
    hours = int(padTime(str(getHours())))
    minutes = int(padTime(str(rtc.get_minutes())))
    ahours = int(alarm_time[0:2])
    aminutes = int(alarm_time[2:4])
    if not alarm_flag:
        if (hours >= ahours) & (minutes >= aminutes):
            print("ALARM")
            alarm_sounding = True
            #sound buzzer
            timer.init(freq=3, mode=Timer.PERIODIC, callback=beeper)
            alarm_flag = True
        
def displayClear():
    oled.fill(0)
    oled.show()
    
def displayTime(cursor_pos=None, digits=""):
    global alarm_set
        
    digit_location = (2,33,70,100)
    oled.fill(0)

    oled.blit(listy[int(digits[0])], digit_location[0], 14)
    oled.blit(listy[int(digits[1])], digit_location[1], 14)
    oled.blit(listy[int(digits[2])], digit_location[2], 14)
    oled.blit(listy[int(digits[3])], digit_location[3], 14)
    oled.fill_rect(62, 20, 4, 4, 1)
    oled.fill_rect(62, 39, 4, 4, 1)
    
    if cursor_pos == 0:
        oled.text("ALARM", 0, 0)
    elif cursor_pos == 1:
        oled.text("ALARM", 0, 0)
        oled.fill_rect(2, 60, 57, 2, 1)
    elif cursor_pos == 2:
        oled.text("ALARM", 0, 0)
        oled.fill_rect(70, 60, 57, 2, 1)
    else:
        weekday = rtc.get_weekday("long")
        date = str(rtc.get_date("ordinal"))
        month = rtc.get_month("long")
        oled.text(weekday, 0, 0)
        oled.text(date + " " + month, 0, 54)
        
    if alarm_set:
        oled.blit(bell,118,0)
    
    oled.show()

def setAlarm():
    global snooze_pressed, plus_pressed, minus_pressed, alarm_pressed, alarm_time
    cursor_pos = 1
    displayTime(cursor_pos, alarm_time)

    hours = int(alarm_time[0:2])
    minutes = int(alarm_time[2:4])
    time_string = padTime(str(hours)) + padTime(str(minutes))
    start_time = time.time()
    while (time.time() - start_time) < 5:
        if snooze_pressed:
            snooze_pressed = False
            break
        
        if plus_pressed:
            plus_pressed = False
            if cursor_pos == 1:
                hours = hours + 1
            else:
                minutes = minutes + 1
                
            if minutes == 60:
                minutes = 0
            elif hours == 24:
                hours = 0
            
            time_string = padTime(str(hours)) + padTime(str(minutes))
            print(time_string)
            displayTime(cursor_pos, time_string)
            start_time = time.time()
            
        if minus_pressed:
            minus_pressed = False
            if cursor_pos == 1:
                hours = hours - 1
            else:
                minutes = minutes - 1
                
            if minutes == -1:
                minutes = 59
            elif hours == -1:
                hours = 23
            
            time_string = padTime(str(hours)) + padTime(str(minutes))
            print(time_string)
            displayTime(cursor_pos, time_string)
            start_time = time.time()
            
        if alarm_pressed:
            alarm_pressed = False
            print("moving cursor right")
            if cursor_pos == 1:
                cursor_pos = 2
            else:
                cursor_pos = 1
            time_string = padTime(str(hours)) + padTime(str(minutes))
            displayTime(cursor_pos, time_string)
            start_time = time.time()
            
        time.sleep(0.1)
    alarm_time = time_string    
    displayClear()
    return
    
    
button_alarm.irq(trigger=machine.Pin.IRQ_FALLING, handler=alarmHandler)
button_plus.irq(trigger=machine.Pin.IRQ_FALLING, handler=plusHandler)
button_minus.irq(trigger=machine.Pin.IRQ_FALLING, handler=minusHandler)
button_snooze.irq(trigger=machine.Pin.IRQ_FALLING, handler=snoozeHandler)

while True:
    if alarm_pressed:
        if count >= 2:
            setAlarm()
            count = 0
        else:
            #need to toggle alarm
            if alarm_set:
                alarm_set = False
            else:
                alarm_set = True
            displayTime(cursor_pos = 0, digits=alarm_time)
            time.sleep(5)
            displayClear()
        alarm_pressed = False

        
    if alarm_set:
        checkAlarm()
            
    if snooze_pressed:
        snooze_pressed = False
        if alarm_sounding:
            # stop noise
            timer.deinit()
            pwm.deinit()
            alarm_sounding = False
            snooze_enabled = True
        else:
            hours = padTime(str(getHours()))
            minutes = padTime(str(rtc.get_minutes()))
            displayTime(digits = hours+minutes)
            time.sleep(5)
            displayClear()
            
    if alarm_flag:
        hours = int(padTime(str(getHours())))
        if hours == "00":
            alarm_flag = False
        
    time.sleep(0.1)