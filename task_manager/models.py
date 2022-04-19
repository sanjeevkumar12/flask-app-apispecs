from datetime import datetime

from sqlalchemy import event, select
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper, backref

from app.core.db import Model
from app.core.utils.text import random_str, slugify
from app.extensions import db

from .types import TaskPriority, TaskStatus


class TodoList(Model):
    __tablename__ = "todo_lists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(244), nullable=False)
    description = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="todo_lists")
    tasks = db.relationship("Task", back_populates="todo_list")
    slug = db.Column(db.String(244), unique=True)

    def __repr__(self):
        return "<TodoList: {}".format(self.title)


class Task(Model):
    __tablename__ = "todo_list_tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(244), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.LOW)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.DRAFT)
    planned_start_date = db.Column(db.DateTime(timezone=True), nullable=True)
    planned_end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    actual_start_date = db.Column(db.DateTime(timezone=True), nullable=True)
    actual_end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    order = db.Column(db.Integer, default=1)
    slug = db.Column(db.String(244), unique=True)
    todo_list_id = db.Column(db.Integer, db.ForeignKey("todo_lists.id"))
    todo_list = db.relationship("TodoList", back_populates="tasks")

    def __repr__(self):
        return "<Task: {}".format(self.title)


@event.listens_for(TodoList, "before_insert")
def create_todo_slug(mapper: Mapper, connection: Connection, target: Model):
    slug = "{}-{}".format(target.title[:100], target.user_id)
    todolist_table = TodoList.__table__
    slug_search = slugify(slug)
    while True:
        row = connection.execute(
            select(todolist_table)
            .where(todolist_table.c.slug == slug_search)
            .order_by(todolist_table.c.slug.desc())
        ).fetchone()
        if row:
            slug_search = "{slug}-{randstr}".format(
                slug=slug, randstr=random_str(6).lower()
            )
            continue
        break
    target.slug = slug_search


@event.listens_for(Task, "before_insert")
def create_task_slug(mapper: Mapper, connection: Connection, target: Model):
    slug = "{}-{}".format(target.title[:100], target.todo_list_id)
    task_table = Task.__table__
    slug_search = slugify(slug)
    while True:
        row = connection.execute(
            select(task_table)
            .where(task_table.c.slug == slug_search)
            .order_by(task_table.c.slug.desc())
        ).fetchone()
        if row:
            slug_search = "{slug}-{randstr}".format(
                slug=slug, randstr=random_str(6).lower()
            )
            continue
        break
    target.slug = slug_search
