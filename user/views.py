from typing import TYPE_CHECKING
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
from passlib.hash import pbkdf2_sha256
import uuid

if TYPE_CHECKING:
    from quart.wrappers.response import Response

from user.models import user_table, get_user_by_username

user_app = Blueprint("user_app", __name__)


@user_app.route("/register", methods=["GET", "POST"])
async def register() -> "Response":
    error: str = ""
    username: str = ""
    password: str = ""
    csrf_token: uuid.UUID = uuid.uuid4()

    if request.method == "GET":
        session["csrf_token"] = str(csrf_token)

    if request.method == "POST":
        form: dict = await request.form
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
async def login() -> "Response":
    error: str = ""
    username: str = ""
    password: str = ""
    csrf_token: uuid.UUID = uuid.uuid4()

    if request.method == "GET":
        session["csrf_token"] = str(csrf_token)
        if request.args.get("next"):
            session["next"] = request.args.get("next")

    if request.method == "POST":
        form: dict = await request.form
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            error = "Please enter username and password"
        else:
            if (
                session.get("csrf_token") != form.get("csrf_token")
                and not current_app.testing
            ):
                error = "Invalid POST contents"

        conn = current_app.dbc

        if not error:
            # check if the user exists
            user = await get_user_by_username(conn, form.get("username"))
            if not user:
                error = "User not found"
            # check the password
            elif not pbkdf2_sha256.verify(password, user.get("password")):
                error = "User not found"

        if not error:
            # login the user
            if not current_app.testing:
                del session["csrf_token"]

            session["user_id"] = user.get("id")
            session["username"] = user.get("username")

            if "next" in session:
                next = session.get("next")
                session.pop("next")
                return redirect(next)
            else:
                return redirect(url_for("home_app.init"))
        else:
            session["csrf_token"] = str(csrf_token)

    return await render_template(
        "user/login.html", error=error, username=username, csrf_token=csrf_token
    )


@user_app.route("/logout", methods=["GET"])
async def logout() -> "Response":
    del session["user_id"]
    del session["username"]
    return redirect(url_for(".login"))
