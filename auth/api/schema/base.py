from marshmallow import Schema, fields, pre_load, validate


class TokenSchema(Schema):
    access_token = fields.String(dump_only=True)
    expire_at = fields.Integer(
        dump_only=True,
        description="Token Expire in milliseconds",
    )
    token_type = fields.String(dump_only=True, validate=validate.OneOf(["Bearer"]))

    class Meta:
        ordered = True


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    slug = fields.String(dump_only=True)

    class Meta:
        ordered = True


class UserTokenSchema(Schema):
    user = fields.Nested(UserSchema)
    token = fields.Nested(TokenSchema)

    class Meta:
        ordered = True
