from quart import Blueprint, render_template

from user.models import user_table

user_app = Blueprint("user_app", __name__)


@user_app.route("/register")
async def register():
    return await render_template("user/register.html")
