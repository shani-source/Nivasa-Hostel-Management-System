from datetime import datetime

from app.extensions import db


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    enrollment_no = db.Column(
        db.String(50),
        unique=True,
        nullable=True
    )

    course = db.Column(
        db.String(100),
        nullable=True
    )

    branch = db.Column(
        db.String(100),
        nullable=True
    )

    year = db.Column(
        db.Integer,
        nullable=True
    )

    gender = db.Column(
        db.String(20),
        nullable=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    address = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "student_profile",
            uselist=False
        )
    )