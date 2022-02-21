from flask import jsonify
from webargs.flaskparser import use_args, use_kwargs

from app.extensions.api import views

from ..blueprints import auth_blueprint
from ..schema.register import RegisterSchema


class RegisterAPIView(views.APIView):
    @use_kwargs(RegisterSchema(), location="json")
    def post(self, **kwargs):
        """Register View
        ---
        description: Register User
        requestBody:
            description: User Details
            content:
                application/json:
                    schema: RegisterSchema
        responses:
            200:
                content:
                    application/json:
                        schema: RegisterSchema
        """
        return jsonify(kwargs)
