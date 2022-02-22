from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...services import auth_repository
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
                        schema: UserToken
            422:
                content:
                    application/json:
                        schema: APIError
        """
        user = auth_repository.get_user_by_email(kwargs.get("email"))
        if user and user.check_password(kwargs.get("password")):
            return {
                "user": user,
                "token": auth_repository.create_user_token(user),
            }, HTTPStatus.OK
        return {
            "messages": {"auth": f"The given credentials are not valid"},
            "error": True,
        }, HTTPStatus.UNPROCESSABLE_ENTITY
