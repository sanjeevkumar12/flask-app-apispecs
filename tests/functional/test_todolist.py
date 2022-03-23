from flask import Flask
from pytest import fixture, mark, raises

from app.core.http.exceptions.api import UnprocessableEntityException
from task_manager.models import Task
from task_manager.services import todo_list_repository

from ..factories.user import UserFactory


class TestTodoList(object):
    def __init__(self):
        self.todo_list_repository = todo_list_repository
        self.user = UserFactory.create()

    @mark.api
    def test_create_todo_list(self):
        todo_list = self.todo_list_repository.create(
            title="To do list", description="No Description", user_id=self.user.id
        )
        assert todo_list.title == "To do list"
        assert todo_list.user == self.user
