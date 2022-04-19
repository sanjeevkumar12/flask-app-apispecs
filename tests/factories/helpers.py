import random
import string
from typing import Any, TypedDict


def random_password(length=10) -> str:
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = "@#$"
    _all = lower + upper + num + symbols
    temp = (
        random.sample(lower, 1)
        + random.sample(upper, 1)
        + random.sample(symbols, 1)
        + random.sample(num, 1)
        + random.sample(_all, length - 4)
    )
    return "".join(temp)


class LoggedInUser(TypedDict):
    email: str
    first_name: str
    last_name: str
    id: int
    slug: str


class LoggedInToken(TypedDict):
    access_token: str
    expire_at: str
    token_type: str


class LoggedInState(TypedDict):
    user: LoggedInUser
    token: LoggedInToken
