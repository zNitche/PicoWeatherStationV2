# Original adafruit_ahtx0 https://github.com/adafruit/Adafruit_CircuitPython_AHTx0/blob/main/adafruit_ahtx0.py
# modified to work with micropython and rpi pico
# Inspired by https://github.com/targetblank/micropython_ahtx0/blob/master/ahtx0.py


import utime

AHTX0_I2CADDR_DEFAULT = 0x38  # Default I2C address
AHTX0_CMD_CALIBRATE = 0xBE  # Calibration command
AHTX0_CMD_TRIGGER = 0xAC  # Trigger reading command
AHTX0_CMD_SOFTRESET = 0xBA  # Soft reset command
AHTX0_STATUS_BUSY = 0x80  # Status bit for busy
AHTX0_STATUS_CALIBRATED = 0x08  # Status bit for calibrated


class AHT20:
    def __init__(self, i2c, address=AHTX0_I2CADDR_DEFAULT):
        utime.sleep_ms(20)  # 20ms delay to wake up

        self.address = address
        self.i2c = i2c
        self.buf = bytearray(6)
        self.reset()

        if not self.calibrate():
            raise RuntimeError("Could not calibrate")

    def is_device_accessible(self):
        return True if self.address in self.i2c.scan() else False

    def reset(self):
        self.buf[0] = AHTX0_CMD_SOFTRESET
        self.i2c.writeto(self.address, self.buf[0:1])

        utime.sleep_ms(20)  # 20ms delay to wake up

    def calibrate(self):
        self.buf[0] = AHTX0_CMD_CALIBRATE
        self.buf[1] = 0x08
        self.buf[2] = 0x00

        self.i2c.writeto(self.address, self.buf[0:3])

        self.wait_for_idle()

        if not self.status() & AHTX0_STATUS_CALIBRATED:
            return False

        return True

    def status(self):
        self.read_to_buffer()

        return self.buf[0]

    def get_relative_humidity(self):
        self.read_data()

        humidity = ((self.buf[1] << 12) | (self.buf[2] << 4) | (self.buf[3] >> 4))
        humidity = (humidity * 100) / 0x100000

        return humidity

    def get_temperature(self):
        self.read_data()

        temp = ((self.buf[3] & 0xF) << 16) | (self.buf[4] << 8) | self.buf[5]
        temp = ((temp * 200.0) / 0x100000) - 50

        return temp

    def trigger_data_read(self):
        self.buf[0] = AHTX0_CMD_TRIGGER
        self.buf[1] = 0x33
        self.buf[2] = 0x00
        self.i2c.writeto(self.address, self.buf[0:3])

    def wait_for_idle(self):
        while self.status() & AHTX0_STATUS_BUSY:
            utime.sleep_ms(5)

    def read_data(self):
        self.trigger_data_read()
        self.wait_for_idle()
        self.read_to_buffer()

    def read_to_buffer(self):
        self.i2c.readfrom_into(self.address, self.buf)
