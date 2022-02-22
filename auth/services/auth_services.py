import typing
from datetime import datetime, timedelta

import jwt
from flask import current_app as app

from app.core.services.sqlalchemy import SqlAlchemyAdaptor
from app.core.utils.security import ipaddress

from ..models import User


class AuthServiceRepository(SqlAlchemyAdaptor):
    entity = User

    def create(self, commit=True, **kwargs) -> User:
        user = User(**kwargs)
        user.password = kwargs.get("password")
        self.session.add(user)
        if commit:
            self.session.commit()
        return user

    def get_user_by_email(self, email) -> typing.Union[User, None]:
        return self.entity.query.filter_by(email=email).first()

    def create_user_token(self, user: User):
        expire_at = timedelta(minutes=app.config.get("JWT_SESSION_MAX_TIME_IN_MINUTES"))
        now = datetime.utcnow()
        payload = {
            "sub": user.email,
            "iat": now,
            "exp": now + expire_at,
            "secure_number": ipaddress.get_user_encoded_ip_address(),
        }
        token = jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")
        return {
            "access_token": token,
            "token_type": "Bearer",
            "expire_at": expire_at.total_seconds() * 1000,
        }

    def decode_auth_token(self, auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: bool|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
