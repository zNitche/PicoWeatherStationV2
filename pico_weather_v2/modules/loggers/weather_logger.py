from pico_weather_v2.modules.loggers.logger_base import LoggerBase
from pico_weather_v2.config import Config
from pico_weather_v2.utils import csv_utils, files_utils


class WeatherLogger(LoggerBase):
    def __init__(self, logs_per_hour, sensors_manager):
        super().__init__()

        self.sensors_manager = sensors_manager

        self.logs_per_hour = logs_per_hour
        self.logging_schedule = self.get_logging_schedule()

        self.last_logged = None

    def timer_callback(self):
        datetime = self.sensors_manager.get_datetime()

        logs_content = csv_utils.get_csv_content(self.get_logs_path())
        last_logged_iso_time = logs_content[-1]["DATETIME"] if len(logs_content) > 0 else None

        if last_logged_iso_time is None:
            self.log_sensors_data()

        else:
            for schedule_time in self.logging_schedule:
                schedule_hour = schedule_time[0]
                schedule_minute = schedule_time[1]

                if schedule_hour == datetime.hour and schedule_minute == datetime.minutes:
                    last_log_time = last_logged_iso_time.split("T")[-1].split(":")
                    last_log_hour = int(last_log_time[0])
                    last_log_minutes = int(last_log_time[1])

                    if not (last_log_hour == datetime.hour and last_log_minutes == datetime.minutes):
                        self.log_sensors_data()
                        break

    def get_logging_schedule(self):
        schedule = []

        for hour in range(24):
            minutes_every_log = 60 // self.logs_per_hour
            current_minutes = 0

            for _ in range(self.logs_per_hour):
                schedule.append([hour, current_minutes])
                current_minutes += minutes_every_log

        return schedule

    def get_logged_rows_count(self):
        return csv_utils.get_rows_count(self.get_logs_path())

    def get_logs_header(self):
        return ["DATETIME", "TEMPERATURE", "HUMIDITY", "BATTERY_VOLTAGE", "PV_VOLTAGE"]

    def get_log_row(self):
        temp, humi = self.sensors_manager.get_temp_and_humidity()
        bat_volt = self.sensors_manager.get_battery_voltage()
        pv_volt = self.sensors_manager.get_pv_voltage()
        datetime = self.sensors_manager.get_datetime().to_iso_string()

        row = f"{datetime},{temp},{humi},{bat_volt},{pv_volt}"

        return row

    def get_logs_path(self):
        datetime = self.sensors_manager.get_datetime()
        day_date = datetime.to_iso_string().split("T")[0]

        return f"{Config.WEATHER_LOGS_DIR_PATH}/{day_date}.csv"

    def log_sensors_data(self):
        files_utils.create_dir_if_doesnt_exit(Config.WEATHER_LOGS_DIR_PATH)

        log_path = self.get_logs_path()

        if not files_utils.check_if_exists(log_path):
            csv_utils.init_csv_file(log_path, self.get_logs_header())

        csv_utils.write_row(log_path, self.get_log_row())

        self.last_logged = self.sensors_manager.get_datetime().to_iso_string()
