from datetime import datetime

from app.extensions import db


class Notice(db.Model):

    __tablename__ = "notices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False,
        default="General"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )