from libs.aht20 import AHT20
from libs.ds3231 import DS3231


class SensorsManager:
    def __init__(self, i2c):
        self.i2c = i2c

        self.aht20 = AHT20(self.i2c)
        self.rtc = DS3231(self.i2c)
