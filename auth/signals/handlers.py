from auth.models import User
from ..utils.mail import send_register_user_email


def _user_register(sender, user: User, token : str, *args, **kwargs):
    send_register_user_email(user=user,token=token)
