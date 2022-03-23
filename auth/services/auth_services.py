import typing
from datetime import datetime, timedelta

import jwt
from flask import current_app as app

from app.core.http.exceptions.api import UnprocessableEntityException
from app.core.services.sqlalchemy import SqlAlchemyAdaptor
from app.core.utils.security import ipaddress
from app.core.utils.security.token import (
    create_time_bound_token_for_value,
    decode_token,
)

from ..models import BlacklistToken, User
from ..types import UserLoginToken
from ..utils.mail import send_forgot_password_token
from ..signals import USER_REGISTER_SIGNAL


class AuthServiceRepository(SqlAlchemyAdaptor):
    entity = User

    def create(self, commit=True, **kwargs) -> User:
        user = User(**kwargs)
        user.password = kwargs.get("password")
        self.session.add(user)
        if commit:
            self.session.commit()
            USER_REGISTER_SIGNAL.send(app, user=user)
        return user

    def get_user_by_email(self, email) -> typing.Union[User, None]:
        return self.entity.query.filter_by(email=email).first()

    def create_user_token(self, user: User) -> UserLoginToken:
        expire_at = timedelta(minutes=app.config.get("JWT_SESSION_MAX_TIME_IN_MINUTES"))
        now = datetime.utcnow()
        payload = {
            "sub": user.email,
            "iat": now,
            "exp": now + expire_at,
            "secure_number": ipaddress.get_user_encoded_ip_address(),
        }
        token = jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")
        return UserLoginToken(
            **{
                "access_token": token,
                "token_type": "Bearer",
                "expire_at": expire_at.total_seconds() * 1000,
            }
        )

    def decode_auth_token(self, auth_token) -> typing.Union[str, bool, None]:
        """
        Validates the auth token
        :param auth_token:
        :return: bool|string
        """
        try:
            payload = jwt.decode(
                auth_token, app.config.get("SECRET_KEY"), algorithms=["HS256"]
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def user_from_auth_token(self, auth_token) -> typing.Union[User, bool, None]:
        token = self.decode_auth_token(auth_token)
        if token:
            return self.entity.query.filter_by(email=token).first()
        return False

    def change_password(
        self, user: User, current_password: str, new_password: str
    ) -> User:
        if user and user.check_password(current_password):
            user.password = new_password
            user.save_to_db()
            return user
        raise UnprocessableEntityException(
            message="The current password is wrong.",
            payload={"auth": "The current password is wrong."},
        )

    def authenticate_user(self, email: str, password: str) -> typing.Union[User, None]:
        user = self.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        raise UnprocessableEntityException(
            message="The given credential are not valid",
            payload={"auth": "The given credential are not valid."},
        )

    def forgot_password_email(
        self,
        email: str,
    ):
        user = self.get_user_by_email(email)
        token, hash = create_time_bound_token_for_value(user.id)
        if user:
            send_forgot_password_token(user=user, token=token)
        return token, hash

    def forgot_password_reset(self, token_hash: str, token: str, new_password):
        token_decoded = decode_token(token_hash)
        user_id, decoded_token, expire = token_decoded.split("-")
        user = self.get_by_id(user_id)
        expire_date_time_utc = int(expire) + 300
        current_timestamp = int(datetime.utcnow().timestamp())
        if (
            user
            and str(token) == str(decoded_token)
            and expire_date_time_utc >= int(current_timestamp)
        ):
            user.password = new_password
            user.save_to_db()
            return user
        raise UnprocessableEntityException(
            message="The given token is not valid or expired.",
            payload={"token": "The given token is not valid or expired."},
        )

    def update_user(self, user: User, first_name: str, last_name: str):
        user.first_name = first_name
        user.last_name = last_name
        user.save_to_db()
        return user

    def mark_token_expire(self, token):
        if token:
            black_list_token = BlacklistToken(token)
            black_list_token.save_to_db()
