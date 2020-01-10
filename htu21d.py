from machine import I2C, Pin
import time

class HTU21D(object):
    I2CADDR = 0x40
    CMD_READTEMP = 0xE3
    CMD_READHUM = 0xE5
    CMD_WRITEREG = 0xE6
    CMD_READREG = 0xE7
    CMD_RESET = 0xFE

    def __init__(self, scl, sda, freq=10000):
        self.i2c = I2C(scl=scl, sda=sda, freq=freq)
        self.reset()
        # User registers should be 0x02 after a reset
        assert(self.userreg == b'\x02')

    def _crc_check(self, value):
        """CRC check data

        Notes:
            stolen from https://github.com/sparkfun/HTU21D_Breakout

        Args:
            value (bytearray): data to be checked for validity

        Returns:
            True if valid, False otherwise
        """
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def _issue_measurement(self, command):
        assert(self.i2c.writeto(self.I2CADDR, bytes([command])) == 1)
        time.sleep_ms(50) # gotta give it time to do its thing
        data = self.i2c.readfrom(self.I2CADDR, 3)
        if not self._crc_check(data):
            raise ValueError()
        raw = (data[0] << 8) + data[1]
        raw &= 0xFFFC
        return raw

    def reset(self):
        self.i2c.writeto(self.I2CADDR, bytes([self.CMD_RESET]))
        return

    @property
    def temperature(self):
        """Calculate temperature"""
        raw = self._issue_measurement(self.CMD_READTEMP)
        return -46.85 + (175.72 * raw / 65536)

    @property
    def humidity(self):
        """Calculate humidity"""
        raw =  self._issue_measurement(self.CMD_READHUM)
        return -6 + (125.0 * raw / 65536)

    @property
    def userreg(self):
        """User Register"""
        return self.i2c.readfrom_mem(self.I2CADDR, self.CMD_READREG, 1)
