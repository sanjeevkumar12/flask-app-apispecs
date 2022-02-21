from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from marshmallow import Schema

from ..security import api_key_scheme, jwt_scheme


class OpenAPISpecs(object):
    def __init__(self, app: Flask = None):
        self.app = None
        self.api_docs = APISpec(
            title="API's",
            version="1.0.0",
            openapi_version="3.0.2",
            info=dict(description="A minimal API"),
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )
        self.view_path = []
        self.schemas = {}

    def init_app(self, app: Flask):
        self.app = app
        self.api_docs.components.security_scheme("api_key", api_key_scheme)
        self.api_docs.components.security_scheme("jwt", jwt_scheme)

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
