from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response
from pico_weather_v2.utils import csv_utils, files_utils
from pico_weather_v2.config import Config
import os
import json


weather_api = Blueprint("weather_api", url_prefix="/api/weather")


@weather_api.route("/logged_days", methods=["GET"])
def logged_days(request):
    logged_days = []

    for file_name in os.listdir(Config.WEATHER_LOGS_DIR_PATH):
        if file_name.endswith(".csv"):
            logged_days.append(file_name.split(".")[0])

    return Response(payload=json.dumps(logged_days))


@weather_api.route("/logs/<day>", methods=["GET"])
def logs(request):
    logs_file_path = f"{Config.WEATHER_LOGS_DIR_PATH}/{request.path_parameters.get('day')}.csv"

    if files_utils.check_if_exists(logs_file_path):
        logs_content = csv_utils.get_csv_content(logs_file_path)
        weather_logger = weather_api.current_app.weather_logger

        return Response(payload=json.dumps({
            "headers": weather_logger.get_logs_header(),
            "logs": logs_content
        }))

    else:
        return weather_api.current_app.raise_error(404)
