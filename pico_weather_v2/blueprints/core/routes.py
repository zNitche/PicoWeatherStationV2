from strawberry.routes.blueprint import Blueprint
from strawberry.utils import routes_utils


core = Blueprint("core", templates_dir="/pico_weather_v2/blueprints/core/templates")


@core.route("/", methods=["GET"])
def home(request):
    sensors_manager = core.current_app.sensors_manager

    temp, humi = sensors_manager.get_temp_and_humidity()
    bat_volt = sensors_manager.get_battery_voltage()
    pv_volt = sensors_manager.get_pv_voltage()

    datetime = sensors_manager.get_datetime().to_iso_string()

    context = {
        "temp": temp,
        "humi": humi,
        "pv_voltage": pv_volt,
        "bat_voltage": bat_volt,
        "datetime": datetime
    }

    return routes_utils.render_template(core.get_template_path("index.html"), context)
