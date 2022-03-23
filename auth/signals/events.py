from app.extensions import signals
from .handlers import _user_register
USER_REGISTER_SIGNAL = signals.register_signal('user.register', _user_register)