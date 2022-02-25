from flask import Flask

from app.conf import settings
from app.extensions import init_extensions

from .views import home_page


def create_app(env: str = "development"):
    app = Flask(__name__)

    try:
        config_object = settings[env]
        app.config.from_object(config_object)
        app.logger.info(f"App Initialized with {env} environment")
        app.logger.info("Config Settings : %s ", app.config.items())
        init_extensions(app)
        app.add_url_rule("/", "home", home_page)
        return app
    except KeyError:
        raise Exception(
            f'{env} not found . Available option are {",".join(settings.keys())}'
        )
