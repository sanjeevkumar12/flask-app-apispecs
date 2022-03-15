import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Config(object):
    BASE_DIR: Path = BASE_DIR
    DEBUG: bool = False
    TESTING: bool = False
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_USE_TLS: bool = True
    MAIL_PORT: int = 2525
    MAIL_DEBUG: bool = int(os.environ.get("MAIL_DEBUG"))
    MAIL_USE_SSL: bool = False
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.environ.get("MAIL_DEFAULT_SENDER")
    SECRET_KEY: str = os.environ.get("APP_SECRET_KEY")
    API_TITLE: str = os.environ.get("API_TITLE")
    APP_ENCRYPTION_KEY: str = os.environ.get("APP_ENCRYPTION_KEY")
    API_VERSION: str = os.environ.get("API_VERSION")
    API_DESCRIPTION: str = os.environ.get("API_DESCRIPTION")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    JWT_SESSION_MAX_TIME_IN_MINUTES = int(
        os.environ.get("JWT_SESSION_MAX_TIME_IN_MINUTES", 30)
    )


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG: bool = True


class TestingConfig(Config):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_TESTING_URI")


settings = {
    "production": "app.conf.ProductionConfig",
    "development": "app.conf.DevelopmentConfig",
    "testing": "app.conf.TestingConfig",
}

API_BLUEPRINTS = ["auth.api.auth_blueprint", "task_manager.api.task_manager_blueprint"]

MODEL_LOOKUP_EXCLUDE_DIRECTORY = ["migrations"]
