from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...services import auth_repository
from ..schema.base import UserTokenSchema
from ..schema.login import LoginSchema


class LoginAPIView(views.APIView):
    @use_kwargs(LoginSchema(), location="json")
    def post(self, **kwargs):
        """Login API View
        ---
        description: Login User
        summary: Login User API
        title: Login
        tags:
            - Auth
            - User
        requestBody:
            description: User Details
            content:
                application/json:
                    schema: Login
        responses:
            200:
                content:
                    application/json:
                        schema: Token
            422:
                content:
                    application/json:
                        schema: APIError
        """
        user = auth_repository.authenticate_user(
            kwargs.get("email"), kwargs.get("password")
        )
        user_schema = UserTokenSchema()
        return (
            user_schema.dump(
                {
                    "user": user,
                    "token": auth_repository.create_user_token(user),
                }
            ),
            HTTPStatus.OK,
        )
