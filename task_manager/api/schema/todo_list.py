from marshmallow import Schema, fields


class TodoListSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    archived = fields.Boolean(dump_only=True)
    order = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)

    class Meta:
        ordered = True
