import typing
from app.core.typings.route import Route
from .schema.todo_list_schema import ToDoListSchema
from .endpoints.todo_list import CreateToDoListView

SCHEMA = {"ToDoList": ToDoListSchema}

VIEWS: typing.List[Route] = [
    {"path": "", "view_func": CreateToDoListView.as_view("create-to-do-list")}
]
