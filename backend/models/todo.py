from backend.extensions import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, default=False)
