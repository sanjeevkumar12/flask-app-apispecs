from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...decorator import token_required
from ...services import auth_repository
from ..schema.password import ChangePasswordSchema, ForgotPasswordSchema


class ChangePasswordAPIView(views.APIView):
    decorators = [
        token_required,
    ]

    @use_kwargs(ChangePasswordSchema, location="json")
    def get(self, user, **kwargs):
        """Register View
        ---
        description: Register User
        summary: Register User API
        title: Register
        tags:
            - Auth
            - User
        requestBody:
            description: User Details
            content:
                application/json:
                    schema: Register
        responses:
            200:
                content:
                    application/json:
                        schema: Register
            422:
                content:
                    application/json:
                        schema: APIError
        """
        kwargs.pop("confirm_password")
        user = auth_repository.get_user_by_email(kwargs.get("email"))
        return user


class ForgotPasswordAPIView(views.APIView):
    def get(self, **kwargs):
        pass
