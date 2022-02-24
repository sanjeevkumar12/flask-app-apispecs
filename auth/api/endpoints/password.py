from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...decorator import token_required
from ...services import auth_repository
from ..schema.password import (
    ChangePasswordSchema,
    ForgotPasswordResetSchema,
    ForgotPasswordSchema,
)


class ChangePasswordAPIView(views.APIView):
    decorators = [
        token_required,
    ]

    @use_kwargs(ChangePasswordSchema, location="json")
    def post(self, user, **kwargs):
        """Change Password API
        ---
        description: Change Password API
        summary: Change Password API
        title: Change Password
        security:
            - JWT: []
        tags:
            - Auth
            - User
        requestBody:
            description: Provide current and new Password
            content:
                application/json:
                    schema: ChangePassword
        responses:
            200:
                content:
                    application/json:
                        schema: ActionSuccess
            422:
                content:
                    application/json:
                        schema: APIError
        """
        auth_repository.change_password(
            user, kwargs.get("old_password"), kwargs.get("new_password")
        )
        return self.send_success_response(message="Password changed successfully.")


class ForgotPasswordAPIView(views.APIView):
    @use_kwargs(ForgotPasswordSchema, location="json")
    def post(self, **kwargs):
        """Register View
        ---
        description: Forgot Password API
        summary: Forgot Password API
        title: Forgot Password
        tags:
            - Auth
            - User
        requestBody:
            description: Forgot Password Request
            content:
                application/json:
                    schema: ForgotPassword
        responses:
            200:
                description: Ok
                content:
                    application/json:
                        schema: ActionSuccess
                        example:
                            message : Please check your email for otp for change password token.
                            error: false
                            payload:
                                token : acb3b6a6cfc975fd5c13e1c1056206e11ee817
                                expire : 100000
            422:
                content:
                    application/json:
                        schema: APIError
        """
        _, hash = auth_repository.forgot_password_email(kwargs.get("email"))
        return self.send_success_response(
            message="Please check your email for otp for change password token.",
            payload={"token_hash": hash},
        )


class ForgotPasswordResetAPIView(views.APIView):
    @use_kwargs(ForgotPasswordResetSchema, location="json")
    def post(self, **kwargs):
        """Register View
        ---
        description: Forgot Password Reset API
        summary: Forgot Password Reset API
        title: Forgot Password Reset
        tags:
            - Auth
            - User
        requestBody:
            description: Forgot Password Reset
            content:
                application/json:
                    schema: ForgotPasswordReset
        responses:
            200:
                description: Ok
                content:
                    application/json:
                        schema: ActionSuccess
                        example:
                            message : Password change success.
                            error: false

            422:
                content:
                    application/json:
                        schema: APIError
        """
        _, hash = auth_repository.forgot_password_reset(
            token=kwargs.get("token"),
            token_hash=kwargs.get("token_hash"),
            new_password=kwargs.get("new_password"),
        )
        return self.send_success_response(message="Password change success.")
