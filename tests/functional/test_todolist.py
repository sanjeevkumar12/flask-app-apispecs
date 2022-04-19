from flask import Flask
from pytest import fixture, mark, raises

from app.core.http.exceptions.api import UnprocessableEntityException
from auth.models import User
from task_manager.models import Task
from task_manager.services import todo_list_repository

from ..factories.helpers import random_password
from ..factories.user import UserFactory


@fixture(scope="module")
def api_user() -> User:
    password = random_password(10)
    user = UserFactory.create(password=password)
    user.raw_password = password
    return user


class TestTodoList(object):
    @mark.api
    def test_create_todo_list(self, api_user):
        todo_list = todo_list_repository.create(
            title="To do list", description="No Description", user_id=api_user.id
        )
        assert todo_list.title == "To do list"
        assert todo_list.user == api_user
        assert not todo_list.archived
