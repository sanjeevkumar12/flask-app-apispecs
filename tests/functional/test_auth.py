from unittest import mock

from flask import Flask
from pytest import fixture, raises

from app.core.http.exceptions.api import UnprocessableEntityException
from auth.models import User
from auth.services import auth_repository

from ..factories.helpers import random_password
from ..factories.user import UserFactory


@fixture(scope="module")
def test_user() -> User:
    password = random_password(10)
    user = UserFactory.build(password=password)
    user.raw_password = password
    return user


def test_create_user(app: Flask, test_user):
    with app.app_context():
        created_user = auth_repository.create(
            commit=True,
            **{
                "email": test_user.email,
                "password": test_user.raw_password,
                "first_name": test_user.first_name,
                "last_name": test_user.last_name,
            },
        )
        assert test_user.email == created_user.email
        assert created_user.check_password(test_user.raw_password)
        test_user.id = created_user.id


def test_authenticate_user(app: Flask, test_user):
    with app.app_context():
        user = auth_repository.authenticate_user(
            email=test_user.email, password=test_user.raw_password
        )
        assert user.id == test_user.id


def test_invalid_username_password(app: Flask, logger):
    with app.app_context():
        with raises(UnprocessableEntityException) as e_info:
            password = random_password(10)
            user = UserFactory.build(password=password)
            auth_repository.authenticate_user(email=user.email, password=user.password)
        logger.info(
            f"Message : {e_info.value.message} , Status : {e_info.value.status_code} "
        )


def test_forgot_password(mocker, app: Flask, test_user, logger):
    with app.app_context(), app.test_request_context():
        mocker.patch(
            "auth.services.auth_services.send_forgot_password_token", return_value=True
        )
        password = random_password(10)
        token, token_hash = auth_repository.forgot_password_email(test_user.email)
        user = auth_repository.forgot_password_reset(token_hash, token, password)
        assert user.check_password(password)
