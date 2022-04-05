from http import HTTPStatus

from http import HTTPStatus

from webargs.flaskparser import use_kwargs

from app.extensions.api import views

from ..schema import todo_list_schema
from auth.decorator import token_required


class CreateToDoListView(views.APIView):
    decorators = [
        token_required,
    ]

    @use_kwargs(todo_list_schema.ToDoListSchema(), location="json")
    def post(self, **kwargs):
        """Create To do List API View
        ---
        description: Create To do List API View
        summary: Create To do List API View
        title: Create To do List
        security:
            - JWT: []
        tags:
            - Todo List

        requestBody:
            description: Todo List Details
            content:
                application/json:
                    schema: ToDoList
        responses:
            200:
                content:
                    application/json:
                        schema: ToDoList
            422:
                content:
                    application/json:
                        schema: APIError
        """
