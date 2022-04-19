from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.core.http.exceptions.api import NotFoundException
from app.extensions.api import views
from auth.decorator import token_required

from ...services import todo_list_repository
from ..schema.todo_list import TodoListSchema


class CreateTodoListAPIView(views.APIView):
    decorators = [
        token_required,
    ]

    @use_kwargs(TodoListSchema, location="json")
    def post(self, user, **kwargs):
        """CCreate To DO List
        ---
        description: Create To DO List
        summary: Create To DO List
        title: Create To DO List
        security:
            - JWT: []
        tags:
            - Todo
        requestBody:
            description: Todo List Detail
            content:
                application/json:
                    schema: TodoList
        responses:
            201:
                description: The resource was created successfully.
                content:
                    application/json:
                        schema: TodoList
            401:
                content:
                    application/json:
                        schema: APIError
        """
        todo_list = todo_list_repository.create(
            user=user, title=kwargs.get("title"), description=kwargs.get("description")
        )
        todo_list_schema = TodoListSchema()
        return todo_list_schema.dump(todo_list), HTTPStatus.CREATED

    @use_kwargs(TodoListSchema, location="json")
    def patch(self, todo_id: int, user, **kwargs):
        """Update To DO List
        ---
        description: Update To DO List
        summary: Update To DO List
        title: Update To DO List
        parameters:
            -   in: path
                name: todo_id
                schema:
                    type: integer
                    required: true
                description: Numeric ID of the user to get
        security:
            - JWT: []
        tags:
            - Todo
        requestBody:
            description: Todo List Detail
            content:
                application/json:
                    schema: TodoList
        responses:
            200:
                description: The resource was updated successfully.
                content:
                    application/json:
                        schema: TodoList
            401:
                content:
                    application/json:
                        schema: APIError
            404:
                content:
                    application/json:
                        schema: APIError
        """
        todo_list = todo_list_repository.get_by_id(todo_id)
        if not todo_list or not todo_list.user == user:
            raise NotFoundException(message="To do list not found")
        todo_list = todo_list_repository.update(
            todo_list=todo_list,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
        )
        todo_list_schema = TodoListSchema()
        return todo_list_schema.dump(todo_list), HTTPStatus.OK
