from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response


core = Blueprint("core")


@core.route("/", methods=["GET"])
def home(request):
    return Response(200, payload="Home")
