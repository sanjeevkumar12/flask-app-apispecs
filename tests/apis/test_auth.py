from flask import Flask

from auth.services import auth_repository


def test_create_user(app: Flask):
    with app.app_context():
        user = auth_repository.create(
            email="sanjumassal@gmail.com", password="1234567", commit=False
        )
        assert user.email == "sanjumassal@gmail.com"
        assert not user.password_hash == "1234567"
        assert user.check_password("1234567")
