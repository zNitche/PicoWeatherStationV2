from libs.aht20 import AHT20
from libs.ds3231 import DS3231
from pico_weather_v2.config import Config
from pico_weather_v2 import utils
import machine
import uos


class SensorsManager:
    def __init__(self, i2c, logs_dir_path=None):
        self.i2c = i2c
        self.logs_timer = machine.Timer()

        self.logs_dir_path = logs_dir_path

        self.aht20 = AHT20(self.i2c)
        self.rtc = DS3231(self.i2c)

        self.bat_adc = machine.ADC(28)
        self.pv_adc = machine.ADC(27)

    def init_logs_timer(self):
        if not utils.check_if_exists(self.logs_dir_path):
            uos.mkdir(self.logs_dir_path)

        self.logs_timer.init(period=2000, mode=machine.Timer.PERIODIC, callback=lambda t: self.log_sensors_data())

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

    def get_log_row(self):
        temp, humi = self.get_temp_and_humidity()
        bat_volt = self.get_battery_voltage()
        pv_volt = self.get_pv_voltage()
        datetime = self.get_datetime().to_iso_string()

        row = f"{datetime},{temp},{humi},{bat_volt},{pv_volt}"

        return row

    def log_sensors_data(self):
        if self.logs_dir_path:
            day_date = self.get_datetime().to_iso_string().split("T")[0]
            log_path = f"{self.logs_dir_path}/{day_date}.txt"

            with open(log_path, "a+") as logs_file:
                logs_file.write(self.get_log_row() + "\n")
