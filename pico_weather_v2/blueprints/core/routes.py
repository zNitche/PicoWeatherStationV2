from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response


core = Blueprint("core")


@core.route("/", methods=["GET"])
def home(request):
    sensors_manager = core.current_app.sensors_manager

    return Response(200, payload=f"tmp: {sensors_manager.aht20.get_temperature()}")
