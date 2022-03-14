from functools import wraps

from flask import request

from app.core.http.exceptions.api import UnauthorizedException

from .services import auth_repository
from .utils.token import get_auth_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_auth_token()
        if not token:
            raise UnauthorizedException(message="Unauthorized Access!")
        try:
            current_user = auth_repository.user_from_auth_token(token)
        except Exception:
            raise UnauthorizedException(message="Unauthorized Access!")
        if not current_user:
            raise UnauthorizedException(message="Unauthorized Access!")
        kwargs.update({"user": current_user})
        return f(*args, **kwargs)

    return decorated
