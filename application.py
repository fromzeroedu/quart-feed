from quart import Quart

from db import db_connection


def create_app(**config_overrides):
    app = Quart(__name__)

    # load config
    app.config.from_pyfile("settings.py")

    # import blueprints
    from home.views import home_app
    from user.views import user_app

    # register blueprints
    app.register_blueprint(home_app)
    app.register_blueprint(user_app)

    @app.before_serving
    async def create_db_conn():
        database = await db_connection()
        await database.connect()
        app.dbc = database

    @app.after_serving
    async def close_db_conn():
        await app.dbc.disconnect()

    return app
