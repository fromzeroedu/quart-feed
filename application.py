from quart import Quart


def create_app(**config_overrides):
    app = Quart(__name__)

    # load config
    app.config.from_pyfile("settings.py")

    # import blueprints
    from home.views import home_app

    # register blueprints
    app.register_blueprint(home_app)

    return app
