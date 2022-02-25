import json
from dataclasses import dataclass
from http import HTTPStatus

from flask import Flask, url_for
from flask.testing import FlaskClient
from pytest import fixture

from auth.services import auth_repository


@fixture
def api_user_data() -> dict:
    return {
        "email": "api-user@gmail.com",
        "first_name": "API",
        "last_name": "Kumar",
        "password": "test@123",
    }


@fixture
def api_user(api_user_data):
    return auth_repository.create(commit=True, **api_user_data)


@fixture
def login_data(app: Flask, client: FlaskClient, api_user_data):
    with app.app_context(), app.test_request_context():
        email = api_user.email
        password = "test@123"
        response = client.post(
            url_for("api.auth.login"),
            data=json.dumps(
                {
                    "email": email,
                    "password": password,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.OK


def test_create_user(app: Flask, client: FlaskClient):
    with app.app_context(), app.test_request_context():
        email = "test_create_user@gmail.com"
        password = "test@123"
        response = client.post(
            url_for("api.auth.register"),
            data=json.dumps(
                {
                    "email": email,
                    "password": password,
                    "confirm_password": password,
                    "first_name": "Sanjeev",
                    "last_name": "Kumar",
                }
            ),
            content_type="application/json",
        )
        user = auth_repository.get_user_by_email(email=email)

        assert response.status_code == HTTPStatus.CREATED
        assert user.email == email


def test_login(app: Flask, client: FlaskClient, api_user):
    with app.app_context(), app.test_request_context():
        email = "test_create_user@gmail.com"
        password = "test@123"
        response = client.post(
            url_for("api.auth.login"),
            data=json.dumps(
                {
                    "email": email,
                    "password": password,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.OK
