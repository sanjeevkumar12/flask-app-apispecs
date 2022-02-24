from datetime import datetime
from random import randrange

from flask import current_app as app

from app.core.utils.security.cryptography import decrypt_message, encrypt_message


def create_token_with_hash(raw_string=None, token_length=6):
    value = (
        raw_string
        if raw_string
        else "".join([str(randrange(1, 9, 1)) for i in range(token_length)])
    )
    hashed_value = encrypt_message(value, app.config.get("APP_ENCRYPTION_KEY").encode())
    return value, hashed_value


def create_time_bound_token_for_value(value, token_length=6):
    value = "".join(
        [str(value), "-"]
        + [str(randrange(1, 9, 1)) for i in range(token_length)]
        + ["-", str(int(datetime.utcnow().timestamp()))]
    )
    _, hashed_value = create_token_with_hash(value)
    return value.split("-")[1], hashed_value


def decode_token(token):
    token = decrypt_message(token, app.config.get("APP_ENCRYPTION_KEY").encode())
    return token
