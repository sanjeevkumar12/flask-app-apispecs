from flask import Flask

from app.conf import settings
from app.extensions import init_extensions


def create_app(env: str = "development"):
    app = Flask(__name__)

    try:
        config_object = settings[env]
        app.config.from_object(config_object)
        app.logger.info(f"App Initialized with {env} environment")
        app.logger.info("Config Settings : %s ", app.config.items())
        app.config["MAIL_SERVER"] = "smtp.mailtrap.io"
        app.config["MAIL_PORT"] = 2525
        app.config["MAIL_USERNAME"] = "4c882d203d04f1"
        app.config["MAIL_PASSWORD"] = "8e00561cb6cbb8"
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USE_SSL"] = False
        init_extensions(app)
        return app
    except KeyError:
        raise Exception(
            f'{env} not found . Available option are {",".join(settings.keys())}'
        )
