from datetime import datetime

from sqlalchemy import event, select
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper
from werkzeug.security import check_password_hash, generate_password_hash

from app.core.db import Model
from app.core.utils.text import random_str, slugify
from app.extensions import db


class User(Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    slug = db.Column(db.String(244), unique=True)
    email = db.Column(db.String(244), unique=True)
    password_hash = db.Column(db.String(244))

    def __repr__(self):
        return "<User: {}>".format(self.email)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class BlacklistToken(Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return "<BlacklistToken: {}".format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


@event.listens_for(User, "before_insert")
def create_username(mapper: Mapper, connection: Connection, target: Model):
    slug = "{}-{}".format(target.first_name, target.last_name)
    user_table = User.__table__
    slug_search = slugify(slug)
    while True:
        row = connection.execute(
            select(user_table)
            .where(user_table.c.slug == slug_search)
            .order_by(user_table.c.slug.desc())
        ).fetchone()
        if row:
            slug_search = "{slug}-{randstr}".format(
                slug=slug, randstr=random_str(6).lower()
            )
            continue
        break
    target.slug = slug_search
