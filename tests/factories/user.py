import json
import typing

import factory
from flask import Flask, url_for
from flask.testing import FlaskClient

from app.extensions import get_session
from auth.models import User

from .helpers import LoggedInState, random_password


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(random_password)
    id = factory.Sequence(lambda n: n)

    class Meta:
        model = User
        sqlalchemy_session = get_session()

    @staticmethod
    def build_invalid_users_for_register() -> typing.List[User]:
        return [
            UserFactory.build(email="invalid email"),
            UserFactory.build(password="in"),
            UserFactory.build(first_name=""),
        ]
