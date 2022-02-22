import typing

from app.core.services.sqlalchemy import SqlAlchemyAdaptor

from ..models import User


class AuthServiceRepository(SqlAlchemyAdaptor):
    entity = User

    def create(self, commit=True, **kwargs) -> User:
        user = User(**kwargs)
        user.password = kwargs.get("password")
        self.session.add(user)
        if commit:
            self.session.commit()
        return user

    def get_user_by_email(self, email) -> typing.Union[User, None]:
        return self.entity.query.filter_by(email=email).first()

    def create_user_token(self, user: User):
        return {}
