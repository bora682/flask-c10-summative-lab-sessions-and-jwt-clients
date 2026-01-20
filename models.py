from datetime import datetime

from sqlalchemy.orm import validates
from marshmallow import Schema, fields

from config import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True, nullable=False)

    _password_hash = db.Column(db.String, nullable=False)

    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # --- validations ---
    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError("Username is required.")
        return username.strip()

    # --- password hashing ---
    @property
    def password_hash(self):
        return self._password_hash

    def set_password(self, password: str):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password: str) -> bool:
        if not password:
            return False
        return bcrypt.check_password_hash(self._password_hash, password)


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="tasks")

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title is required.")
        return title.strip()


# --- Marshmallow Schemas (for JSON responses) ---

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()


class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str(allow_none=True)
    completed = fields.Bool()
    created_at = fields.DateTime()
