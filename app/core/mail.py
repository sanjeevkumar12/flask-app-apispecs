import typing

from flask_mail import Message

from app.extensions import mail


def send_message(to: typing.Union[str, list], subject: str, message, **kwargs):
    from_add = kwargs.get("from", mail.app.config.get("MAIL_DEFAULT_SENDER"))
    to = to if isinstance(to, list) else [to]
    msg = Message(subject, sender=from_add, recipients=to)
    msg.body = message
    msg.html = message
    mail.send(msg)
