from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ...decorator import token_required
from ...services import auth_repository
from ..schema.base import UserProfileSchema


class UserProfileUpdateView(views.APIView):
    decorators = [
        token_required,
    ]

    @use_kwargs(UserProfileSchema, location="json")
    def patch(self, user, **kwargs):
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
            201:
                description: The resource was deleted successfully.
            401:
                content:
                    application/json:
                        schema: APIError
        """
        auth_repository.update_user(
            user, first_name=kwargs.get("first_name"), last_name=kwargs.get("last_name")
        )
        return ({}, HTTPStatus.CREATED)
