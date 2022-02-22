from functools import wraps

from flask import request

from .services import auth_repository


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return "Unauthorized Access!", 401

        try:
            current_user = auth_repository.decode_auth_token(token)
            if not current_user:
                return "Unauthorized Access!", 401
            kwargs.update({"user": current_user})
        except Exception:
            return "Unauthorized Access!", 401
        return f(*args, **kwargs)

    return decorated
