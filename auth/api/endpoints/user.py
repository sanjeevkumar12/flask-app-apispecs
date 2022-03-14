from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...decorator import token_required
from ...services import auth_repository
from ...utils.token import get_auth_token
from ..schema.base import UserProfileSchema, UserSchema


class CurrentUserAPIView(views.APIView):
    decorators = [
        token_required,
    ]

    def get(self, user, **kwargs):
        """Current User View
        ---
        description: User Detail
        summary: User Detail API
        title: User Details
        security:
            - JWT: []
        tags:
            - User
        responses:
            200:
                content:
                    application/json:
                        schema: User
            401:
                content:
                    application/json:
                        schema: APIError
        """
        user_schema = UserSchema()
        return (
            user_schema.dump(user),
            HTTPStatus.OK,
        )

    @use_kwargs(UserProfileSchema, location="json")
    def patch(self, user, **kwargs):
        """Current User View
        ---
        description: User Detail Update
        summary: User Detail Update
        title: User Detail Update
        security:
            - JWT: []
        requestBody:
            description: User Details
            content:
                application/json:
                    schema: UserProfileSchema
        tags:
            - User
        responses:
            201:
                description: The resource was updated successfully.
            401:
                content:
                    application/json:
                        schema: APIError
        """
        auth_repository.update_user(
            user, first_name=kwargs.get("first_name"), last_name=kwargs.get("last_name")
        )
        return ({}, HTTPStatus.CREATED)


class UserLogoutView(views.APIView):
    decorators = [
        token_required,
    ]

    def get(self, user, **kwargs):
        """Expire Current Token
        ---
        description: User Logout
        summary:  User Logout
        title:  User Logout
        security:
            - JWT: []
        tags:
            - User
        responses:
            204:
                description: No Content
            401:
                content:
                    application/json:
                        schema: APIError
        """
        auth_repository.mark_token_expire(get_auth_token())
        return (
            None,
            HTTPStatus.OK,
        )
