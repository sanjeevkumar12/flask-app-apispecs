from flask import url_for

from app.extensions.api import openapi

from .blueprints import auth_blueprint
from .endpoints.register import RegisterAPIView
from .schema.register import RegisterSchema

openapi.open_api_docs.register_schema("RegisterSchema", RegisterSchema)

register_view = RegisterAPIView.as_view("register")
auth_blueprint.add_url_rule("/register", view_func=register_view)
openapi.open_api_docs.add_view_to_doc(register_view)
