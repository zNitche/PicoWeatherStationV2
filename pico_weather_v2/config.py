class Config:
    DEBUG = False

    HOTSPOT_SSID = "pw_1"
    HOTSPOT_PASSWORD = "123456789"

    SD_CARD_MOUNT_DIR = "/sd"

    ADC_CONVERSION_FACTOR = 3.3 / 65535
    PV_VOLTAGE_DIVIDER_FACTOR = 6  # 1V ON ADC PIN = 6V OF SOURCE VOLTAGE
    BAT_VOLTAGE_DIVIDER_FACTOR = 2  # 1V ON ADC PIN = 2V OF SOURCE VOLTAGE

    SENSORS_ACCURACY = 1

    WEATHER_LOGS_DIR_PATH = f"{SD_CARD_MOUNT_DIR}/weather_logs"
    WEATHER_LOGGER_TIMER_PERIOD = 30000
    WEATHER_LOGS_PER_HOUR = 3
