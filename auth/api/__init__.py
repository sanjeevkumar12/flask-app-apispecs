from app.extensions.api import openapi

from .blueprints import auth_blueprint
from .endpoints.login import LoginAPIView
from .endpoints.password import (
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    ForgotPasswordResetAPIView,
)
from .endpoints.profile import UserProfileUpdateView
from .endpoints.register import RegisterAPIView
from .endpoints.user import CurrentUserAPIView, UserLogoutView
from .schema.base import TokenSchema, UserProfileSchema, UserSchema, UserTokenSchema
from .schema.password import (
    ChangePasswordSchema,
    ForgotPasswordResetSchema,
    ForgotPasswordSchema,
)
from .schema.register import LoginSchema, RegisterSchema

openapi.open_api_docs.register_schema("Register", RegisterSchema)
openapi.open_api_docs.register_schema("Token", TokenSchema)
openapi.open_api_docs.register_schema("ChangePassword", ChangePasswordSchema)
openapi.open_api_docs.register_schema("ForgotPassword", ForgotPasswordSchema)
openapi.open_api_docs.register_schema("ForgotPasswordReset", ForgotPasswordResetSchema)
openapi.open_api_docs.register_schema("UserProfile", UserProfileSchema)

openapi.open_api_docs.register_schema("Login", LoginSchema)

register_view = RegisterAPIView.as_view("register")
login_view = LoginAPIView.as_view("login")
user_me_view = CurrentUserAPIView.as_view("me")
forgot_password_view = ForgotPasswordAPIView.as_view("forgot_password")
forgot_password_reset_view = ForgotPasswordResetAPIView.as_view("forgot_password_reset")
change_password_view = ChangePasswordAPIView.as_view("change_password")
logout_view = UserLogoutView.as_view("logout")


auth_blueprint.add_url_rule("/register", view_func=register_view)
openapi.open_api_docs.add_view_to_doc(register_view)

auth_blueprint.add_url_rule("/login", view_func=login_view)
openapi.open_api_docs.add_view_to_doc(login_view)

auth_blueprint.add_url_rule("/me", view_func=user_me_view)
openapi.open_api_docs.add_view_to_doc(user_me_view)

auth_blueprint.add_url_rule("/forgot-password", view_func=forgot_password_view)
openapi.open_api_docs.add_view_to_doc(forgot_password_view)

auth_blueprint.add_url_rule(
    "/forgot-password/reset", view_func=forgot_password_reset_view
)
openapi.open_api_docs.add_view_to_doc(forgot_password_reset_view)

auth_blueprint.add_url_rule("/change-password", view_func=change_password_view)
openapi.open_api_docs.add_view_to_doc(change_password_view)

auth_blueprint.add_url_rule("/logout", view_func=logout_view)
openapi.open_api_docs.add_view_to_doc(logout_view)
