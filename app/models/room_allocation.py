from datetime import datetime

from app.extensions import db


class RoomAllocation(db.Model):

    __tablename__ = "room_allocations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    allocation_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "room_allocations",
            lazy=True
        )
    )

    room = db.relationship(
        "Room",
        backref=db.backref(
            "allocations",
            lazy=True
        )
    )