import typing

from app.core.services.sqlalchemy import SqlAlchemyAdaptor

from ..models import Task, TodoList


class TodoListServiceRepository(SqlAlchemyAdaptor):
    entity = TodoList

    def get_all(self) -> typing.List[TodoList]:
        return self.entity.query.all()

    def create(self, *, title, description, user_id) -> TodoList:
        task_list = self.entity(title=title, description=description, user_id=user_id)
        task_list.save_to_db()
        return task_list

    def get_all_task_for_todo_list(self, todo_list_id: int) -> typing.List[TodoList]:
        return (
            Task.query.filter(Task.todo_list_id == todo_list_id)
            .order_by(Task.order.asc())
            .all()
        )
