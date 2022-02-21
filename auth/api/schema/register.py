from marshmallow import Schema, fields, pre_load


class RegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    confirm_password = fields.String(required=True)

    class Meta:
        ordered = True

    @pre_load
    def process_input(self, data, **kwargs):
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return data
