import factory

from app.extensions import get_session
from auth.models import User

from .helpers import random_password


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(random_password)
    id = factory.Sequence(lambda n: n)

    class Meta:
        model = User
        sqlalchemy_session = get_session()
