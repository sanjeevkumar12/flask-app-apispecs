from flask import g, request
from flask.views import MethodView
from flask.wrappers import Request as BaseRequest


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
