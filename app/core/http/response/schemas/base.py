from marshmallow import fields, schema


class APIErrorSchema(schema.Schema):
    messages = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
    error = fields.Boolean(required=False, default=True)
    description = fields.Str(required=False)
