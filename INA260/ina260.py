import struct
from machine import Pin, I2C

#Registers
_REG_CONFIG = 0x00  # CONFIGURATION REGISTER (R/W)
_REG_CURRENT = 0x01  # SHUNT VOLTAGE REGISTER (R)
_REG_VOLTAGE = 0x02  # BUS VOLTAGE REGISTER (R)
_REG_POWER = 0x03  # POWER REGISTER (R)
_REG_MASK_ENABLE = 0x06  # MASK ENABLE REGISTER (R/W)
_REG_ALERT_LIMIT = 0x07  # ALERT LIMIT REGISTER (R/W)
_REG_MFG_UID = 0xFE  # MANUFACTURER UNIQUE ID REGISTER (R)
_REG_DIE_UID = 0xFF  # DIE UNIQUE ID REGISTER (R)

#Config register settings
#RST, -, -, -, AVG2, AVG1, AVG0, BVCT2, BVCT1, BVCT0, SVCT2, SVCT1, SVCT0, M3, M2, M1

#Averaging mode
average_mode = {'AVG_1': 0b000000000000,
                'AVG_4' : 0b001000000000,
                'AVG_16' : 0b010000000000,
                'AVG_64' : 0b011000000000,
                'AVG_128' : 0b100000000000,
                'AVG_256' : 0b101000000000,
                'AVG_512' : 0b110000000000,
                'AVG_1024' : 0b111000000000}

#Bus Voltage conversion time us
bvct = {'BVCT_140' : 0b000000000,
        'BVCT_204' : 0b001000000,
        'BVCT_332' : 0b010000000,
        'BVCT_588' : 0b011000000,
        'BVCT_1100' : 0b100000000,
        'BVCT_2116' : 0b101000000,
        'BVCT_4156' : 0b110000000,
        'BVCT_8244' : 0b111000000}

#Shunt Voltage conversion time us
svct = {'SVCT_140' : 0b000000,
        'SVCT_204' : 0b001000,
        'SVCT_332' : 0b010000,
        'SVCT_588' : 0b011000,
        'SVCT_1100' : 0b100000,
        'SVCT_2116' : 0b101000,
        'SVCT_4156' : 0b110000,
        'SVCT_8244' : 0b111000}

#Operating mode
op_mode = {'SHUTDOWN' : 0b000,
            'SV_TRIG' : 0b001,
            'BV_TRIG' : 0b010,
            'SBV_TRIG' : 0b011,
            'SV_CONT' : 0b101,
            'BV_CONT' : 0b110,
            'SBV_CONT' : 0b111}

TEXAS_INSTRUMENT_ID = 0x5449
INA260_ID = 0x2270
CONFIG_REG = 0b0110000100100111


class INA260:
    def __init__(self, i2c=None, address=0x40):
        self.i2c = i2c
        self.address = address
    
    def _read(self, reg):
        data = self.i2c.readfrom_mem(self.address, reg, 2)
        res = struct.unpack('>H',bytearray(data))[0]
        return(res)
    
    def _write(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, value.to_bytes(2, "big"))
        return
    
    def _write_config(self, value):
        config_value = self._read(_REG_CONFIG)
        config_value = config_value | value
        self._write(_REG_CONFIG, config_value)

    def _del_(self):
        self.i2c.close()
        
    def is_triggered(self):
        res = self._read(_REG_MASK_ENABLE)
        #check if bit 3 is true
        if res & (1 << 3):
            return True
        else:
            return False

    def current(self):
        res = self._read(_REG_CURRENT) * 0.00125
        return res
    
    def voltage(self):
        res = self._read(_REG_VOLTAGE) * 0.00125
        return res
    
    def power(self):
        res = self._read(_REG_POWER) * 0.01
        return res
    
    def reset(self):
        self._write(_REG_CONFIG, 0x8000)
        CONFIG_REG = 0X6127

    def average_mode(self, value):
        self._write_config(average_mode[value])

    def bus_conversion_time(self, value):
        self._write_config(bvct[value])

    def shunt_conversion_time(self, value):
        self._write_config(average_mode[value])

    def operating_mode(self, value):
        self._write_config(op_mode[value])