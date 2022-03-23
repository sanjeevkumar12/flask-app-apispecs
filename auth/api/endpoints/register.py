from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...services import auth_repository
from ..schema.register import RegisterSchema, RegisterActivateUserSchema


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


class RegisterActivateAPIView(views.APIView):
    @use_kwargs(RegisterActivateUserSchema(), location="json")
    def post(self, **kwargs):
        """Register View
        ---
        description: Register Activate User
        summary: Register Activate User API
        title: Activate User
        tags:
            - Auth
            - User
        requestBody:
            description: Activate User Account
            content:
                application/json:
                    schema: RegisterActivateUser
        responses:
            200:
                content:
                    application/json:
                        schema: ActionSuccess
                        example:
                            message : Account activated successfully.
                            error: false
            422:
                content:
                    application/json:
                        schema: APIError
        """
        auth_repository.user_account_activate(
            token=kwargs.get("token"),
            token_hash=kwargs.get("token_hash")
        )
        return self.send_success_response(message="Account activated successfully.")
