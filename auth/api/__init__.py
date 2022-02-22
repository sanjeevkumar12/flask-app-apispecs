from flask import url_for

from app.extensions.api import openapi

from .blueprints import auth_blueprint
from .endpoints.login import LoginAPIView
from .endpoints.register import RegisterAPIView
from .schema.base import TokenSchema, UserSchema, UserTokenSchema
from .schema.register import LoginSchema, RegisterSchema

openapi.open_api_docs.register_schema("Register", RegisterSchema)
openapi.open_api_docs.register_schema("Token", TokenSchema)
openapi.open_api_docs.register_schema("UserToken", UserTokenSchema)

openapi.open_api_docs.register_schema("Login", LoginSchema)

register_view = RegisterAPIView.as_view("register")
login_view = LoginAPIView.as_view("login")

auth_blueprint.add_url_rule("/register", view_func=register_view)
openapi.open_api_docs.add_view_to_doc(register_view)

auth_blueprint.add_url_rule("/login", view_func=login_view)
openapi.open_api_docs.add_view_to_doc(login_view)
