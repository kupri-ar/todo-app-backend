from marshmallow import fields

from models import TodoItem, ma


class TodoItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TodoItem
        load_instance = True

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    content = fields.Str(required=True)
    is_checked = fields.Boolean()
