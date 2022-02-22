import os


def test_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "SQLALCHEMY_DATABASE_TESTING_URI"
    )
