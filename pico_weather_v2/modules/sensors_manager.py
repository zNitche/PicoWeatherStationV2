from libs.aht20 import AHT20
from libs.ds3231 import DS3231
from pico_weather_v2.config import Config
import machine


class SensorsManager:
    def __init__(self, i2c, logs_dir_path=None):
        self.i2c = i2c

        self.logs_dir_path = logs_dir_path

        self.aht20 = AHT20(self.i2c)
        self.rtc = DS3231(self.i2c)

        self.bat_adc = machine.ADC(28)
        self.pv_adc = machine.ADC(27)

    def get_voltage_from_adc(self, adc, voltage_divider_factor):
        adc_value = adc.read_u16()
        adc_voltage = adc_value * Config.ADC_CONVERSION_FACTOR

        voltage = adc_voltage * voltage_divider_factor
        voltage = voltage if voltage >= 0 else 0

        return round(voltage, Config.SENSORS_ACCURACY)

    def get_battery_voltage(self):
        return self.get_voltage_from_adc(self.bat_adc, Config.BAT_VOLTAGE_DIVIDER_FACTOR)

    def get_pv_voltage(self):
        return self.get_voltage_from_adc(self.pv_adc, Config.PV_VOLTAGE_DIVIDER_FACTOR)

    def get_temp_and_humidity(self):
        temp = round(self.aht20.get_temperature(), Config.SENSORS_ACCURACY)
        humi = round(self.aht20.get_relative_humidity(), Config.SENSORS_ACCURACY)

        return temp, humi

    def get_datetime(self):
        return self.rtc.get_datetime()
