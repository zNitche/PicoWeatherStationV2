from libs.aht20 import AHT20
from libs.ds3231 import DS3231
from pico_weather_v2.config import Config
import machine


class SensorsManager:
    def __init__(self, i2c):
        self.i2c = i2c

        self.aht20 = AHT20(self.i2c)
        self.rtc = DS3231(self.i2c)

        self.bat_adc = machine.ADC(28)
        self.pv_adc = machine.ADC(27)

    def get_voltage_from_adc(self, adc):
        adc_value = adc.read_u16()
        adc_voltage = adc_value * Config.ADC_CONVERSION_FACTOR

        return adc_voltage * Config.VOLTAGE_DIVIDER_FACTOR - Config.ADC_ACCURACY

    def get_battery_voltage(self):
        return self.get_voltage_from_adc(self.bat_adc)

    def get_pv_voltage(self):
        return self.get_voltage_from_adc(self.pv_adc)

    def get_temp_and_humidity(self):
        temp = self.aht20.get_temperature()
        humi = self.aht20.get_relative_humidity()

        return temp, humi

    def get_datetime(self):
        return self.rtc.get_datetime()

    def log_sensors_data(self):
        pass
