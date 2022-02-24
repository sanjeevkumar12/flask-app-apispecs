import typing

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from marshmallow import Schema

from app.core.http.response.schemas import ActionSuccessSchema, APIErrorSchema

from ..security import jwt_scheme


class OpenAPISpecs(object):
    def __init__(self, app: Flask = None):
        self.app = None
        self.api_docs: typing.Union[APISpec, None] = APISpec(
            title="API's",
            version="1.0.0",
            openapi_version="3.0.2",
            info=dict(description="A minimal API"),
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )
        self.view_path = []
        self.schemas = {}
        self.api_docs.components.security_scheme("JWT", jwt_scheme)
        self.register_schema("APIError", schema=APIErrorSchema)
        self.register_schema("ActionSuccess", schema=ActionSuccessSchema)
        if self.app:
            self._load()

    def init_app(self, app: Flask):
        self.app = app
        self._load()

    def _load(self):
        self.api_docs.title = self.app.config.get("API_TITLE")
        self.api_docs.version = self.app.config.get("API_VERSION")
        self.api_docs.options.update(
            {"info": {"description": self.app.config.get("API_DESCRIPTION")}}
        )

    def register_schema(self, name: str, schema: Schema) -> None:
        self.api_docs.components.schema(name, schema=schema)

    def add_view_to_doc(self, view):
        self.view_path.append(view)

    def to_dict(self):
        with self.app.app_context():
            for view in self.view_path:
                self.api_docs.path(view=view)
        return self.api_docs.to_dict()


open_api_docs = OpenAPISpecs()
