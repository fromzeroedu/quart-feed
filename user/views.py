from quart import (
    Blueprint,
    render_template,
    request,
    session,
    current_app,
    flash,
    redirect,
    url_for,
)
from quart.wrappers.response import Response
from passlib.hash import pbkdf2_sha256
import uuid

from user.models import user_table, get_user_by_username

user_app = Blueprint("user_app", __name__)


@user_app.route("/register", methods=["GET", "POST"])
async def register() -> Response:
    error: str = ""
    username: str = ""
    password: str = ""
    csrf_token: uuid.UUID = uuid.uuid4()

    if request.method == "GET":
        session["csrf_token"] = str(csrf_token)

    if request.method == "POST":
        form = await request.form
        username = form.get("username", "")
        password = form.get("password", "")

        if not username or not password:
            error = "Please enter username and password"
        else:
            if (
                session.get("csrf_token") != form.get("csrf_token")
                and not current_app.testing
            ):
                error = "Invalid POST contents"

            conn = current_app.dbc

            # check if the user exists
            if not error:
                user = await get_user_by_username(conn, username)
                if user and user["id"]:
                    error = "Username already exists"

            # register the user
            if not error:
                if not current_app.testing:
                    del session["csrf_token"]

                hash: str = pbkdf2_sha256.hash(password)
                user_insert = user_table.insert().values(
                    username=username, password=hash
                )
                await conn.execute(query=user_insert)
                await flash("You have been registered, please login")
                return redirect(url_for(".login"))
            else:
                session["csrf_token"] = str(csrf_token)

    return await render_template(
        "user/register.html", error=error, username=username, csrf_token=csrf_token
    )


@user_app.route("/login", methods=["GET", "POST"])
async def login() -> str:
    return "Login page"
