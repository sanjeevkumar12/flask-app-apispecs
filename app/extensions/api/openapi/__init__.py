import typing
from dataclasses import dataclass
from typing import Any, List, Optional

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from marshmallow import Schema

from app.core.http.response.schemas import ActionSuccessSchema, APIErrorSchema

from ..security import jwt_scheme


@dataclass
class APISpecsViewParams(object):
    path: Optional[str]
    operations: Optional[Any]
    summary: Optional[str]
    description: Optional[str]
    parameters: Optional[List]
    view: Optional[Any]
    kwargs: Optional[dict]


class OpenAPISpecs(object):
    def __init__(self, app: Flask = None):
        self.app = app
        self.api_docs: typing.Union[APISpec, None] = APISpec(
            title="API's",
            version="1.0.0",
            openapi_version="3.0.2",
            info=dict(description="A minimal API"),
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )
        self.view_path: List[APISpecsViewParams] = []
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

    def add_view_to_doc(
        self,
        view,
        *,
        path=None,
        operations=None,
        summary=None,
        description=None,
        parameters=None,
        **kwargs
    ):
        api_params = APISpecsViewParams(
            path=path,
            operations=operations,
            summary=summary,
            description=description,
            parameters=parameters,
            view=view,
            kwargs=kwargs,
        )
        self.view_path.append(api_params)

    def to_dict(self):
        with self.app.app_context():
            for params in self.view_path:
                self.api_docs.path(
                    view=params.view,
                    path=params.path,
                    operations=params.operations,
                    parameters=params.parameters,
                    **params.kwargs
                )
        return self.api_docs.to_dict()


open_api_docs = OpenAPISpecs()
