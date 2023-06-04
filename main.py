from strawberry.controllers.server import Server
from strawberry.controllers.app import App
from pico_weather_v2.config import Config
from pico_weather_v2.managers.sensors_manager import SensorsManager
from libs import sdcard
import machine
import uos


def mount_sd_card():
    cs = machine.Pin(9, machine.Pin.OUT)
    spi = machine.SPI(1, baudrate=1000000,
                      polarity=0, phase=0,
                      bits=8, firstbit=machine.SPI.MSB,
                      sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(8))

    card = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(card)
    uos.mount(vfs, Config.SD_CARD_MOUNT_DIR)


def init_managers(app):
    i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

    setattr(app, "sensors_manager", SensorsManager(i2c, Config.WEATHER_LOGS_DIR_PATH))


def create_app():
    app = App(debug_mode=Config.DEBUG, static_files_dirs=["/pico_weather_v2/static",
                                                          f"{Config.SD_CARD_MOUNT_DIR}/static"])
    init_managers(app)

    from pico_weather_v2.blueprints.core.routes import core
    app.register_blueprint(core)

    return app


def main():
    mount_sd_card()

    server = Server(hotspot_mode=True,
                    hotspot_name=Config.HOTSPOT_SSID, hotspot_password=Config.HOTSPOT_PASSWORD,
                    debug_mode=Config.DEBUG)

    server.set_app(create_app())
    server.run()

    server.app.sensors_manager.init_logs_timer()

    server.run_mainloop()


if __name__ == "__main__":
    main()
