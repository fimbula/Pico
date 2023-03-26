import ina260
import struct
from time import sleep
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400_000)
ina = ina260.INA260(i2c=i2c)

while True:
    print(ina.current())
    sleep(1)

