from marshmallow import Schema, fields, pre_load


class ToDoListSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=False)
    archived = fields.Boolean(default=False, dump_only=True)
    order = fields.Integer(default=0, dump_only=True)
    user_id = fields.Integer(default=None, dump_only=True)
    slug = fields.String(dump_only=True)
    id = fields.String(dump_only=True)
