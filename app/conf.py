import os
from pathlib import Path


class Config(object):
    BASE_DIR: Path = Path(__file__).parent.parent
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.environ.get("APP_SECRET_KEY")
    API_TITLE: str = os.environ.get("API_TITLE")
    API_VERSION: str = os.environ.get("API_VERSION")
    OPENAPI_VERSION: str = "3.0.2"
    OPENAPI_URL_PREFIX: str = "/"
    OPENAPI_SWAGGER_UI_PATH: str = "/docs"
    OPENAPI_SWAGGER_UI_URL: str = (
        "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    )

    OPENAPI_RAPIDOC_PATH: str = "/redoc"
    OPENAPI_RAPIDOC_URL: str = (
        "https://cdn.jsdelivr.net/npm/rapidoc/dist/rapidoc-min.js"
    )


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
