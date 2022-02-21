from app.extensions.api import Blueprint

auth_blueprint = Blueprint("auth", "auth", url_prefix="/auth")
