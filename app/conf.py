import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

_DATABASE_SETTINGS = {
    "DB_NAME": os.environ.get("SQLALCHEMY_DATABASE_NAME"),
    "DB_USERNAME": os.environ.get("SQLALCHEMY_DATABASE_USERNAME"),
    "DB_PASS": os.environ.get("SQLALCHEMY_DATABASE_PASSWORD"),
    "DB_PORT": os.environ.get("SQLALCHEMY_DATABASE_PORT"),
    "DB_HOST": os.environ.get("SQLALCHEMY_DATABASE_HOST"),
}

_DATABASE_TEST_SETTINGS = _DATABASE_SETTINGS.copy()
_DATABASE_TEST_SETTINGS["DB_NAME"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_NAME")

_SQLALCHEMY_URI = (
    "postgresql://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        **_DATABASE_SETTINGS
    )
)
_TEST_SQLALCHEMY_URI = (
    "postgresql://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        **_DATABASE_TEST_SETTINGS
    )
)


class Config(object):
    BASE_DIR: Path = BASE_DIR
    DEBUG: bool = False
    TESTING: bool = False
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_USE_TLS: bool = os.environ.get("MAIL_USE_TLS", False).lower() in {
        "1",
        "t",
        "true",
    }
    MAIL_PORT: int = os.environ.get("MAIL_PORT")
    MAIL_DEBUG: bool = int(os.environ.get("MAIL_DEBUG"))
    MAIL_USE_SSL: bool = os.environ.get("MAIL_USE_SSL", False).lower() in {
        "1",
        "t",
        "true",
    }
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.environ.get("MAIL_DEFAULT_SENDER")
    SECRET_KEY: str = os.environ.get("APP_SECRET_KEY")
    API_TITLE: str = os.environ.get("API_TITLE")
    APP_ENCRYPTION_KEY: str = os.environ.get("APP_ENCRYPTION_KEY")
    API_VERSION: str = os.environ.get("API_VERSION")
    API_DESCRIPTION: str = os.environ.get("API_DESCRIPTION")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = _SQLALCHEMY_URI
    JWT_SESSION_MAX_TIME_IN_MINUTES = int(
        os.environ.get("JWT_SESSION_MAX_TIME_IN_MINUTES", 30)
    )


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG: bool = True


class TestingConfig(Config):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI = _TEST_SQLALCHEMY_URI


settings = {
    "production": "app.conf.ProductionConfig",
    "development": "app.conf.DevelopmentConfig",
    "testing": "app.conf.TestingConfig",
}

API_BLUEPRINTS = ["auth.api.auth_blueprint", "task_manager.api.task_manager_blueprint"]

MODEL_LOOKUP_EXCLUDE_DIRECTORY = ["migrations"]
