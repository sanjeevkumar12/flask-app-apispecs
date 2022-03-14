import json
import typing
from http import HTTPStatus

from flask import Flask, url_for
from flask.testing import FlaskClient
from pytest import fixture, mark

from auth.models import User
from auth.services import auth_repository

from ..factories.helpers import random_password
from ..factories.user import UserFactory


def invalid_users_for_register() -> typing.List[User]:
    return UserFactory.build_invalid_users_for_register()


@fixture(scope="module")
def api_user() -> User:
    password = random_password(10)
    user = UserFactory.build(password=password)
    user.raw_password = password
    return user


class TestRegisterUser(object):
    @mark.parametrize("user", invalid_users_for_register())
    def test_invalid_user_register(
        self, user: User, app: Flask, client: FlaskClient, logger
    ):
        with app.app_context(), app.test_request_context():
            logger.info(f"{user.to_dict()}")
            response = client.post(
                url_for("api.auth.register"),
                data=json.dumps(
                    {
                        "email": user.email,
                        "password": user.password,
                        "confirm_password": user.password,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                ),
                content_type="application/json",
            )
            user = auth_repository.get_user_by_email(email=user.email)
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
            assert user is None

    def test_create_user(self, app: Flask, client: FlaskClient, api_user: User, logger):
        with app.app_context(), app.test_request_context():
            logger.info(f"{api_user.to_dict()}")
            response = client.post(
                url_for("api.auth.register"),
                data=json.dumps(
                    {
                        "email": api_user.email,
                        "password": api_user.raw_password,
                        "confirm_password": api_user.raw_password,
                        "first_name": api_user.first_name,
                        "last_name": api_user.last_name,
                    }
                ),
                content_type="application/json",
            )
            user = auth_repository.get_user_by_email(email=api_user.email)
            assert response.status_code == HTTPStatus.CREATED
            assert user.email == api_user.email
            api_user.id = user.id


def test_login(app: Flask, client: FlaskClient, api_user, logger):
    with app.app_context(), app.test_request_context():
        logger.info(f"{api_user.to_dict()}  -> {api_user.raw_password}")
        response = client.post(
            url_for("api.auth.login"),
            data=json.dumps(
                {
                    "email": api_user.email,
                    "password": api_user.raw_password,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.OK
