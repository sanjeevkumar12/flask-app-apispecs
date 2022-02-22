from marshmallow import fields

from .login import LoginSchema


class RegisterSchema(LoginSchema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    confirm_password = fields.String(required=True)

    class Meta:
        ordered = True
