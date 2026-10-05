from datetime import datetime

from app.extensions import db


class LeaveRequest(db.Model):

    __tablename__ = "leave_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    from_date = db.Column(
        db.Date,
        nullable=False
    )

    to_date = db.Column(
        db.Date,
        nullable=False
    )

    reason = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    admin_remark = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "leave_requests",
            lazy=True
        )
    )