from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class TodoItem(db.Model):
    __tablename__ = "todo_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    is_checked = db.Column(db.Boolean(), default=False)
    edited_by_admin = db.Column(db.Boolean(), default=False)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return 'TodoItem: ID<{}>, Content<{}>'.format(self.id, self.name)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "content": self.content,
                "is_checked": self.is_checked,
                "edited_by_admin": self.edited_by_admin,
                "created": self.created,
                "modified": self.modified}

