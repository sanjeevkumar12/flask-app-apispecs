from http import HTTPStatus

from app.extensions.api import views

from ...decorator import token_required
from ..schema.base import UserSchema


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
