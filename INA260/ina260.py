import struct
from machine import Pin, I2C

_REG_CONFIG = 0x00  # CONFIGURATION REGISTER (R/W)
_REG_CURRENT = 0x01  # SHUNT VOLTAGE REGISTER (R)
_REG_VOLTAGE = 0x02  # BUS VOLTAGE REGISTER (R)
_REG_POWER = 0x03  # POWER REGISTER (R)
_REG_MASK_ENABLE = 0x06  # MASK ENABLE REGISTER (R/W)
_REG_ALERT_LIMIT = 0x07  # ALERT LIMIT REGISTER (R/W)
_REG_MFG_UID = 0xFE  # MANUFACTURER UNIQUE ID REGISTER (R)
_REG_DIE_UID = 0xFF  # DIE UNIQUE ID REGISTER (R)

TEXAS_INSTRUMENT_ID = 0x5449
INA260_ID = 0x227


class INA260:
    def __init__(self, i2c=None, address=0x40):
        self.i2c = i2c
        self.address = address
    
    def _read(self, reg):
        data = self.i2c.readfrom_mem(self.address, reg, 2)
        res = struct.unpack('>H',bytearray(data))[0]
        return(res)
    
    def _write(self, reg):
        self.i2c.writeto_mem(self.address, _REG_CONFIG, 2)
        return
    
    def _del_(self):
        self.i2c.close()

    def current(self):
        res = self._read(_REG_CURRENT) * 0.00125
        return res
    
    def voltage(self):
        res = self._read(_REG_VOLTAGE) * 0.00125
        return 
    
    def power(self):
        res = self._read(_REG_POWER) * 0.01
        return
    
    def reset(self):
        self._write(0x8000)