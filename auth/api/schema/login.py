from marshmallow import Schema, fields, pre_load


class LoginSchema(Schema):
    email = fields.Email(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)

    @pre_load
    def process_input(self, data, **kwargs):
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return data
