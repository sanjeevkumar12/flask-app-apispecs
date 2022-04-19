from app.extensions.api import openapi

from .blueprint import task_manager_blueprint
from .endpoints.todo_list import CreateTodoListAPIView
from .schema import todo_list

openapi.open_api_docs.register_schema("TodoList", todo_list.TodoListSchema)

create_to_list_api = CreateTodoListAPIView.as_view("create_to_list")
create_to_list_api_1 = CreateTodoListAPIView.as_view("create_to_list_1")

task_manager_blueprint.add_url_rule(
    "/todo-list", view_func=create_to_list_api, methods=["POST"]
)
task_manager_blueprint.add_url_rule(
    "/todo-list/<string:todo_id>", view_func=create_to_list_api_1, methods=["PATCH"]
)
openapi.open_api_docs.add_view_to_doc(create_to_list_api)
openapi.open_api_docs.add_view_to_doc(create_to_list_api_1)
