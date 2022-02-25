from flask import Flask
from pytest import fixture, raises

from app.core.http.exceptions.api import UnprocessableEntityException
from auth.services import auth_repository


@fixture
def test_user():
    return auth_repository.create(
        email="sanjumassal@gmail.com",
        first_name="sanjeev",
        last_name="kumar",
        password="1234567",
        commit=True,
    )


def test_create_user(app: Flask, test_user):
    with app.app_context():
        assert test_user.email == "sanjumassal@gmail.com"
        assert test_user.check_password("1234567")


def test_authenticate_user(app: Flask, test_user):
    with app.app_context():
        user = auth_repository.authenticate_user(
            email="sanjumassal@gmail.com", password="1234567"
        )
        assert user.id == test_user.id


def test_invalid_username_password(app: Flask, logger):
    with app.app_context():
        with raises(UnprocessableEntityException) as e_info:
            auth_repository.authenticate_user(
                email="non-existing-email@gmail.com", password="1234567"
            )
            logger.info(f"Message : {e_info.message} , Status : {e_info.status_code}")
