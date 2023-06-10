from strawberry.routes.blueprint import Blueprint
from strawberry.utils import routes_utils
import machine


core = Blueprint("core", templates_dir="/pico_weather_v2/blueprints/core/templates")


@core.route("/", methods=["GET"])
def home(request):
    return routes_utils.render_template(core.get_template_path("index.html"), {})


@core.route("/management", methods=["GET"])
def management(request):
    app = core.current_app

    context = {
        "machine_reset_url": app.url_for("core.reset_machine"),
    }

    return routes_utils.render_template(core.get_template_path("management.html"), context)


@core.route("/management/reset_machine", methods=["POST"])
def reset_machine(request):
    machine.reset()
    return routes_utils.redirect(core.current_app.url_for("core.home"))


@core.route("/weather_logs", methods=["GET"])
def logged_weather_days(request):
    performing_log = core.current_app.weather_logger.performing_log

    if performing_log:
        return routes_utils.render_template(core.get_template_path("logging_in_progress.html"), {})
    else:
        return routes_utils.render_template(core.get_template_path("weather_days.html"), {})


@core.route("/weather_logs/<day>", methods=["GET"])
def weather_logs(request):
    day = request.path_parameters.get("day")
    performing_log = core.current_app.weather_logger.performing_log

    if day is None:
        return core.current_app.raise_error(404)

    if performing_log:
        return routes_utils.render_template(core.get_template_path("logging_in_progress.html"), {})
    else:
        return routes_utils.render_template(core.get_template_path("weather_day.html"), {"day": day})
