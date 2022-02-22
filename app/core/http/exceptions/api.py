class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload: dict = None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


class UnauthorizedException(APIException):
    status_code = 401

    def to_dict(self):
        rv = dict()
        rv["messages"] = self.payload if self.payload else {}
        rv["description"] = self.message
        rv["error"] = True
        return rv
