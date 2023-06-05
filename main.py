from strawberry.controllers.server import Server
from pico_weather_v2.config import Config
from pico_weather_v2.app import create_app
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


def main():
    mount_sd_card()

    server = Server(hotspot_mode=True,
                    hotspot_name=Config.HOTSPOT_SSID, hotspot_password=Config.HOTSPOT_PASSWORD,
                    debug_mode=Config.DEBUG)

    server.set_app(create_app())
    server.run()

    server.app.weather_logger.init_timer(periodic=True, period=Config.WEATHER_LOGGER_TIMER_PERIOD)

    server.run_mainloop()


if __name__ == "__main__":
    main()
