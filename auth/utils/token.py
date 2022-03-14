import typing

from flask import request


def get_auth_token() -> typing.Union[str, None]:
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
    if token:
        token = token.split(" ")[-1]
    return token
