from http import HTTPStatus

from flask import Blueprint, Flask, jsonify

from app import conf
from app.core.http.exceptions.api import APIException
from app.core.http.exceptions.handler import handle_api_error, handle_error_422
from app.core.utils.loaders.modules import load_module
from app.extensions.api.openapi import open_api_docs
from app.extensions.api.openapi.views import (
    rapidoc_ui,
    redoc_ui,
    swagger_json,
    swagger_ui,
)

api_blp = Blueprint(
    "api",
    "apis",
    url_prefix="/api/v1",
)


def init_apis(app: Flask):
    app.add_url_rule("/swaggger.json", "swaggger", swagger_json)
    app.add_url_rule("/docs", "swaggger-ui", swagger_ui)
    app.add_url_rule("/redocs", "redoc-ui", redoc_ui)
    app.add_url_rule("/rapidoc", "rapidoc-ui", rapidoc_ui)
    for api_blueprint in conf.API_BLUEPRINTS:
        api_blueprint_obj = load_module(api_blueprint)
        api_blp.register_blueprint(api_blueprint_obj)
    app.register_blueprint(api_blp)
    open_api_docs.init_app(app)

    app.register_error_handler(HTTPStatus.UNPROCESSABLE_ENTITY, handle_error_422)
    app.register_error_handler(APIException, handle_api_error)

    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code


__all__ = ["Blueprint", "init_apis", "open_api_docs"]
