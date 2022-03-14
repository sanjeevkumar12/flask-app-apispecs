from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...services import auth_repository
from ..schema.register import RegisterSchema


class RegisterAPIView(views.APIView):
    @use_kwargs(RegisterSchema(), location="json")
    def post(self, **kwargs):
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
        if user:
            return {
                "messages": {"email": f"{kwargs.get('email')} is not available"},
                "error": True,
            }, HTTPStatus.UNPROCESSABLE_ENTITY
        user = auth_repository.create(**kwargs)
        user_schema = RegisterSchema()
        return user_schema.dump(user), HTTPStatus.CREATED
