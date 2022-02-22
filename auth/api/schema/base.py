from marshmallow import Schema, fields, pre_load


class TokenSchema(Schema):
    access_token = fields.String(dump_only=True)
    access_expire = fields.TimeDelta(dump_only=True)
    token_type = fields.String(dump_only=True)

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
