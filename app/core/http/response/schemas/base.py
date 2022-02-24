from marshmallow import Schema, fields


class APIErrorSchema(Schema):
    messages = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
    error = fields.Boolean(required=False, default=True)
    description = fields.Str(required=False)


class ActionSuccessSchema(Schema):
    message = fields.Str(required=True)
    error = fields.Boolean(default=False)
    payload = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
