from strawberry.controllers.server import Server
from strawberry.controllers.app import App
from pico_weather_v2.config import Config


def create_app():
    app = App(debug_mode=Config.DEBUG)

    from pico_weather_v2.blueprints.core.routes import core

    app.register_blueprint(core)

    return app


def main():
    server = Server(hotspot_mode=True,
                    hotspot_name=Config.HOTSPOT_SSID, hotspot_password=Config.HOTSPOT_PASSWORD,
                    debug_mode=Config.DEBUG)

    server.run()

    server.set_app(create_app())
    server.run_mainloop()


if __name__ == "__main__":
    main()
