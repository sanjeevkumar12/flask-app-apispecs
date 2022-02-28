from typing import TypedDict


class UserLoginToken(TypedDict):
    access_token : str
    token_type : str
    expire_at: float