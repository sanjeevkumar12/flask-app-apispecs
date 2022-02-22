import json
from http import HTTPStatus

from flask import Flask, url_for
from flask.testing import FlaskClient

from auth.services import auth_repository


def test_create_user(app: Flask, client: FlaskClient):
    with app.app_context(), app.test_request_context():
        response = client.post(
            url_for("api.auth.register"),
            data=json.dumps(
                {
                    "email": "test_create_user@gmail.com",
                    "password": "test@123",
                    "confirm_password": "test@123",
                    "first_name": "Sanjeev",
                    "last_name": "Kumar",
                }
            ),
            content_type="application/json",
        )
        print(response.json)
        assert response.status_code == HTTPStatus.CREATED
