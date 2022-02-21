from flask import Flask, jsonify

from app.extensions.api.openapi import open_api_docs

from .api import init_apis
from .database import db, db_migration, get_session, init_db


def init_extensions(app: Flask):
    init_apis(app)
    init_db(app)


__all__ = ["db", "init_extensions", "db_migration", "get_session", "open_api_docs"]
