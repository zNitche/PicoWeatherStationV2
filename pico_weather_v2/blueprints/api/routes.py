from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response
import json


api = Blueprint("api", url_prefix="/api")


@api.route("/sensors", methods=["GET"])
def sensors(request):
    sensors_manager = api.current_app.sensors_manager
    weather_logger = api.current_app.weather_logger

    temp, humidity = sensors_manager.get_temp_and_humidity()
    battery_voltage = sensors_manager.get_battery_voltage()
    pv_voltage = sensors_manager.get_pv_voltage()

    datetime = sensors_manager.get_datetime().to_iso_string()

    readings = {
        "temperature": round(temp, 2),
        "humidity": round(humidity, 2),
        "pv_voltage": round(pv_voltage, 2),
        "battery_voltage": round(battery_voltage, 2),
        "datetime": datetime,
        "last_weather_log": weather_logger.last_logged,
    }

    return Response(payload=json.dumps(readings))
