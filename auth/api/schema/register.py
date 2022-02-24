from marshmallow import ValidationError, fields, validate, validates_schema

from .login import LoginSchema


class RegisterSchema(LoginSchema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(
        required=True, load_only=True, validate=[validate.Length(min=6, max=36)]
    )
    confirm_password = fields.String(required=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if not data["password"] == data["confirm_password"]:
            raise ValidationError(
                {"confirm_password": "Password doesn't matches with confirm password"}
            )

    class Meta:
        ordered = True
