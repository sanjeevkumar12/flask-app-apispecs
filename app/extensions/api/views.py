from http import HTTPStatus

from flask import g, jsonify, request
from flask.views import MethodView
from flask.wrappers import Request as BaseRequest

from app.core.http.response.schemas import ActionSuccessSchema


class Request(BaseRequest):
    user: object


class APIView(MethodView):
    request: Request

    def __init__(self, *args, **kwargs):
        super(APIView, self).__init__(*args, **kwargs)
        self.request = request
        setattr(self.request, "user", g.user if hasattr(g, "user") else None)

    @property
    def user(self):
        if hasattr(self.request, "user"):
            return self.request.user
        return None

    def send_success_response(
        self, message: str, payload=None, status_code=HTTPStatus.OK
    ):
        action_success_schema = ActionSuccessSchema()
        data = {"message": message, "error": False}
        if payload:
            data.update({"payload": payload})
        return (
            jsonify(action_success_schema.dump(data)),
            status_code,
        )
