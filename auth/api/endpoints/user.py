from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...services import auth_repository
from ..schema.login import LoginSchema
