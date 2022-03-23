from flask import Flask, jsonify

from app.extensions.api.openapi import open_api_docs as api_docs

from .api import init_apis
from .database import db, db_migration, get_session, init_db
from .mail import mail
from . import signals


def init_extensions(app: Flask):
    init_apis(app)
    init_db(app)
    mail.init_app(app)
    mail.app = app
    signals.init_signal(app)


__all__ = [
    "db",
    "init_extensions",
    "db_migration",
    "get_session",
    "api_docs",
    "signals",
]
