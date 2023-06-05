import machine
from pico_weather_v2.config import Config
from pico_weather_v2.modules.sensors_manager import SensorsManager
from pico_weather_v2.modules.loggers.weather_logger import WeatherLogger
from strawberry.controllers.app import App


def init_app_modules(app):
    i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

    sensors_manager = SensorsManager(i2c, Config.WEATHER_LOGS_DIR_PATH)

    setattr(app, "sensors_manager", sensors_manager)
    setattr(app, "weather_logger", WeatherLogger(Config.WEATHER_LOGS_PER_HOUR, sensors_manager))


def create_app():
    app = App(debug_mode=Config.DEBUG, static_files_dirs=["/pico_weather_v2/static",
                                                          f"{Config.SD_CARD_MOUNT_DIR}/static"])
    init_app_modules(app)

    from pico_weather_v2.blueprints.core.routes import core
    app.register_blueprint(core)

    return app
