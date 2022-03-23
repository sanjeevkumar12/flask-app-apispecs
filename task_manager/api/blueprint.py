from app.extensions.api import Blueprint

task_manager_blueprint = Blueprint("task_manager", "task_manager", url_prefix="/tasks")
