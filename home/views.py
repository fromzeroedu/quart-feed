from quart import Blueprint, session

home_app = Blueprint("home_app", __name__)


@home_app.route("/", methods=["GET"])
async def init() -> str:
    return "Hello " + str(session.get("username"))
