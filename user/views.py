from quart import Blueprint, current_app


user_app = Blueprint("user_app", __name__)


@user_app.route("/register")
async def register():
    return "<h1>User Registration</h1>"
