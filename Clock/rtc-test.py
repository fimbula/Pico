from machine import Pin, I2C
from time import sleep
import rv3028_rtc
 
sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=machine.I2C(0)
print("I2C Address : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c)) # Display I2C config

rtc=rv3028_rtc.RV3028(0x52, i2c, "LSM")
 
#date_hour = (2021,12,01,16,41,40,"wed")
 
#rtc.set_rtc_date_time(date_hour)

heure = rtc.get_hours()
minute = rtc.get_minutes()
seconde = rtc.get_seconds()
 
joursemaine = rtc.get_weekday(day_type="long")
nommois = rtc.get_month(month_type="short")
datedujour = rtc.get_date(date_type="ordinal")
an = rtc.get_year()
 
heure = str(heure) +":" + str(minute) +":" + str(seconde)
print (heure)
print(joursemaine, datedujour, nommois, an)
