from app.extensions.api import openapi

from .blueprint import task_manager_blueprint


from task_manager.api import meta


def start_app():
    for key, schema in meta.SCHEMA.items():
        openapi.open_api_docs.register_schema(key, schema)
    for route in meta.VIEWS:
        task_manager_blueprint.add_url_rule(route["path"], view_func=route["view_func"])
        openapi.open_api_docs.add_view_to_doc(route["view_func"])


start_app()
