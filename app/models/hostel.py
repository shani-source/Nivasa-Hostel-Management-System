from datetime import datetime

from app.extensions import db


class Hostel(db.Model):

    __tablename__ = "hostels"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    warden_name = db.Column(
        db.String(100),
        nullable=True
    )

    gender = db.Column(
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