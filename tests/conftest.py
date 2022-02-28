from logging import Logger

import pytest
from flask import Flask

from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def logger(app: Flask) -> Logger:
    return app.logger
