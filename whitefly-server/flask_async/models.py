from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(100), nullable=False)

    @validates('name', 'surname')
    def validate_names(self, key, value):
        if any(char.isdigit() for char in value):
            raise ValueError(f"Field '{key}' cannot contain numbers!")
        return value
