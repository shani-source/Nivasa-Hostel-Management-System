from datetime import datetime

from app.extensions import db


class Fee(db.Model):

    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    fee_type = db.Column(
        db.String(50),
        nullable=False,
        default="Hostel Fee"
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    payment_date = db.Column(
        db.Date,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref=db.backref("fees", lazy=True)
    )