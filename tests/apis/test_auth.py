import json
from http import HTTPStatus

from flask import Flask, url_for
from flask.testing import FlaskClient
from pytest import fixture

from auth.models import User
from auth.services import auth_repository

from ..factories.helpers import random_password
from ..factories.user import UserFactory


@fixture(scope="module")
def api_user() -> User:
    password = random_password(10)
    user = UserFactory.build(password=password)
    user.raw_password = password
    return user


def test_create_user(app: Flask, client: FlaskClient, api_user: User):
    with app.app_context(), app.test_request_context():
        print(api_user)
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
        logger.info(api_user.email)
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


def test_forgot_password(app: Flask, client: FlaskClient, api_user, logger):
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
