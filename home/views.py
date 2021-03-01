from quart import Blueprint

home_app = Blueprint("home_app", __name__)


@home_app.route("/", methods=["GET"])
async def init() -> str:
    return "Hello World!"
