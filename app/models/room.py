from datetime import datetime

from app.extensions import db


class Room(db.Model):

    __tablename__ = "rooms"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    hostel_id = db.Column(
        db.Integer,
        db.ForeignKey("hostels.id"),
        nullable=False
    )

    room_number = db.Column(
        db.String(20),
        nullable=False
    )

    floor = db.Column(
        db.Integer,
        nullable=True
    )

    capacity = db.Column(
        db.Integer,
        nullable=False,
        default=4
    )

    occupied = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="available"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    hostel = db.relationship(
        "Hostel",
        backref=db.backref(
            "rooms",
            lazy=True
        )
    )

    @property
    def available_beds(self):

        return max(
            self.capacity - self.occupied,
            0
        )