import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Config(object):
    BASE_DIR: Path = BASE_DIR
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.environ.get("APP_SECRET_KEY")
    API_TITLE: str = os.environ.get("API_TITLE")
    API_VERSION: str = os.environ.get("API_VERSION")
    API_DESCRIPTION: str = os.environ.get("API_DESCRIPTION")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG: bool = True


class TestingConfig(Config):
    TESTING: bool = True


settings = {
    "production": "app.conf.ProductionConfig",
    "development": "app.conf.DevelopmentConfig",
    "testing": "app.conf.TestingConfig",
}

API_BLUEPRINTS = ["auth.api.auth_blueprint"]

MODEL_LOOKUP_EXCLUDE_DIRECTORY = []
