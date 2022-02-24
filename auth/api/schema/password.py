from marshmallow import Schema, fields, pre_load, validate


class ChangePasswordSchema(Schema):

    old_password = fields.String(required=True, load_only=True)
    confirm_password = fields.String(required=True)
    new_password = fields.String(required=True)


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)


class ForgotPasswordResetSchema(Schema):
    token = fields.Str(required=True)
    token_hash = fields.Str(required=True)
    new_password = fields.String(required=True)
