from marshmallow import (
    Schema,
    ValidationError,
    fields,
    pre_load,
    validate,
    validates_schema,
)


class ChangePasswordSchema(Schema):

    old_password = fields.String(required=True, load_only=True)
    confirm_password = fields.String(required=True)
    new_password = fields.String(required=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if not data["confirm_password"] == data["new_password"]:
            raise ValidationError(
                {"new_password": "Password doesn't matches with confirm password"}
            )


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)


class ForgotPasswordResetSchema(Schema):
    token = fields.Str(required=True)
    token_hash = fields.Str(required=True)
    new_password = fields.String(required=True)
