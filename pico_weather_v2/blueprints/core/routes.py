from strawberry.routes.blueprint import Blueprint
from strawberry.utils import routes_utils


core = Blueprint("core", templates_dir="/pico_weather_v2/blueprints/core/templates")


@core.route("/", methods=["GET"])
def home(request):
    return routes_utils.render_template(core.get_template_path("index.html"), {})


@core.route("/weather_logs", methods=["GET"])
def logged_weather_days(request):
    return routes_utils.render_template(core.get_template_path("weather_days.html"), {})


@core.route("/weather_logs/<day>", methods=["GET"])
def weather_logs(request):
    day = request.path_parameters.get("day")

    if day is None:
        return core.current_app.raise_error(404)

    return routes_utils.render_template(core.get_template_path("weather_day.html"), {"day": day})
