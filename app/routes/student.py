from ai.assistant import get_ai_response
from ai.complaint_classifier import classify_complaint
from flask import (Blueprint, render_template, request, redirect, url_for, flash , abort )
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Student , RoomAllocation , Complaint , LeaveRequest ,  Fee , Notice , Notification

student = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)
@student.before_request
def student_only():

    if current_user.is_authenticated:

        if current_user.role != "student":
            abort(403)
@student.context_processor
def inject_notifications():

    if current_user.is_authenticated and current_user.role == "student":

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if student:

            notifications = Notification.query.filter_by(
                student_id=student.id
            ).order_by(
                Notification.created_at.desc()
            ).limit(5).all()

            unread_count = Notification.query.filter_by(
                student_id=student.id,
                is_read=False
            ).count()

            return {
                "notifications": notifications,
                "unread_count": unread_count
            }

    return {
        "notifications": [],
        "unread_count": 0
    }

# ================= DASHBOARD =================

@student.route("/dashboard")
@login_required
def dashboard():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if student_profile is None:
        return "Student profile not found.", 404

    # Get student's complaints
    complaints = Complaint.query.filter_by(
        student_id=student_profile.id
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    # Get student's leave requests
    leave_requests = LeaveRequest.query.filter_by(
        student_id=student_profile.id
    ).order_by(
        LeaveRequest.created_at.desc()
    ).all()

    # Get student's fees
    fees = Fee.query.filter_by(
        student_id=student_profile.id
    ).order_by(
        Fee.due_date.desc()
    ).all()


    # ================= COMPLAINT STATUS COUNTS =================

    pending_complaints = sum(
        1
        for complaint in complaints
        if complaint.status == "Pending"
    )

    in_progress_complaints = sum(
        1
        for complaint in complaints
        if complaint.status == "In Progress"
    )

    resolved_complaints = sum(
        1
        for complaint in complaints
        if complaint.status == "Resolved"
    )


    # ================= LEAVE STATUS COUNTS =================

    pending_leave_requests = sum(
        1
        for leave in leave_requests
        if leave.status == "Pending"
    )

    approved_leave_requests = sum(
        1
        for leave in leave_requests
        if leave.status == "Approved"
    )

    rejected_leave_requests = sum(
        1
        for leave in leave_requests
        if leave.status == "Rejected"
    )


    # ================= PENDING FEES =================

    pending_fees = sum(
        fee.amount
        for fee in fees
        if fee.payment_status == "Pending"
    )


    # ================= RECENT ACTIVITY =================

    activities = []

    for complaint in complaints:
        activities.append({
            "type": "complaint",
            "item": complaint,
            "created_at": complaint.created_at
        })

    for leave in leave_requests:
        activities.append({
            "type": "leave",
            "item": leave,
            "created_at": leave.created_at
        })

    for fee in fees:
        activities.append({
            "type": "fee",
            "item": fee,
            "created_at": fee.created_at
        })


    # Sort newest activity first
    activities.sort(
        key=lambda activity: activity["created_at"],
        reverse=True
    )

    # Show only latest 6 activities
    activities = activities[:6]


    # ================= SEND DATA TO DASHBOARD =================

    return render_template(
        "student/dashboard.html",

        user=current_user,
        student=student_profile,

        complaints=complaints,
        leave_requests=leave_requests,
        fees=fees,

        # Complaint counts
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints,

        # Leave counts
        pending_leave_requests=pending_leave_requests,
        approved_leave_requests=approved_leave_requests,
        rejected_leave_requests=rejected_leave_requests,

        # Fees
        pending_fees=pending_fees,

        # Recent activity
        activities=activities
    )



      
# ================= MY ROOM =================

@student.route("/room")
@login_required
def my_room():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if student_profile is None:
        return "Student profile not found.", 404

    allocation = RoomAllocation.query.filter_by(
        student_id=student_profile.id,
        status="active"
    ).first()

    return render_template(
        "student/room.html",
        user=current_user,
        allocation=allocation
    )

# ================= EDIT PROFILE =================

@student.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        student_profile.enrollment_no = request.form.get(
            "enrollment_no", ""
        ).strip()

        student_profile.course = request.form.get(
            "course", ""
        ).strip()

        student_profile.branch = request.form.get(
            "branch", ""
        ).strip()

        year = request.form.get("year", "").strip()

        student_profile.year = int(year) if year else None

        student_profile.gender = request.form.get(
            "gender", ""
        ).strip()

        student_profile.phone = request.form.get(
            "phone", ""
        ).strip()

        student_profile.address = request.form.get(
            "address", ""
        ).strip()

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("student.edit_profile")
        )

    return render_template(
        "student/edit_profile.html",
        user=current_user,
        student=student_profile
    )
# ================= COMPLAINTS =================

@student.route("/complaints")
@login_required
def complaints():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    complaints = Complaint.query.filter_by(
        student_id=student_profile.id
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        "student/complaints.html",
        user=current_user,
        complaints=complaints
    )


@student.route("/complaints/create", methods=["GET", "POST"])
@login_required
def create_complaint():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        if not title or not description:

            flash(
                "Please fill in the complaint title and description.",
                "error"
            )

            return redirect(
                url_for("student.create_complaint")
            )

        # AI classification
        ai_result = classify_complaint(
            title,
            description
        )

        complaint = Complaint(
            student_id=student_profile.id,
            title=title,
            description=description,
            category=ai_result["category"],
            priority=ai_result["priority"],
            ai_confidence=ai_result["confidence"],
            status="Pending"
        )

        db.session.add(complaint)
        db.session.commit()

        flash(
            "Complaint submitted successfully!",
            "success"
        )

        return redirect(
            url_for("student.complaints")
        )

    return render_template(
        "student/create_complaint.html",
        user=current_user
    )
# ================= LEAVE MANAGEMENT =================

@student.route("/leave")
@login_required
def leave():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    leave_requests = LeaveRequest.query.filter_by(
        student_id=student_profile.id
    ).order_by(
        LeaveRequest.created_at.desc()
    ).all()

    return render_template(
        "student/leave.html",
        user=current_user,
        leave_requests=leave_requests
    )


@student.route("/leave/apply", methods=["GET", "POST"])
@login_required
def apply_leave():

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        reason = request.form.get(
            "reason",
            ""
        ).strip()

        if not from_date or not to_date or not reason:

            flash(
                "Please fill in all leave details.",
                "error"
            )

            return redirect(
                url_for("student.apply_leave")
            )

        from datetime import datetime

        start_date = datetime.strptime(
            from_date,
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            to_date,
            "%Y-%m-%d"
        ).date()

        if end_date < start_date:

            flash(
                "End date cannot be before start date.",
                "error"
            )

            return redirect(
                url_for("student.apply_leave")
            )

        leave_request = LeaveRequest(
            student_id=student_profile.id,
            from_date=start_date,
            to_date=end_date,
            reason=reason
        )

        db.session.add(leave_request)
        db.session.commit()

        flash(
            "Leave request submitted successfully!",
            "success"
        )

        return redirect(
            url_for("student.leave")
        )

    return render_template(

        "student/apply_leave.html",
        user=current_user
    )


# FEES #


@student.route("/fees")
@login_required
def fees():

    student = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    fees = Fee.query.filter_by(
        student_id=student.id
    ).order_by(
        Fee.due_date.desc()
    ).all()

    total_fees = sum(fee.amount for fee in fees)

    paid_fees = sum(
        fee.amount
        for fee in fees
        if fee.payment_status == "Paid"
    )

    pending_fees = total_fees - paid_fees

    return render_template(
        "student/fees.html",
        user=current_user,
        student=student,
        fees=fees,
        total_fees=total_fees,
        paid_fees=paid_fees,
        pending_fees=pending_fees
    )

# =========================
# DEMO FEE PAYMENT
# =========================

@student.route("/fees/<int:fee_id>/pay", methods=["GET", "POST"])
@login_required
def pay_fee(fee_id):

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if student_profile is None:
        return "Student profile not found.", 404

    fee = Fee.query.filter_by(
        id=fee_id,
        student_id=student_profile.id
    ).first_or_404()

    # Prevent paying an already-paid fee
    if fee.payment_status == "Paid":
        flash(
            "This fee has already been paid.",
            "info"
        )
        return redirect(url_for("student.fees"))

    if request.method == "POST":

        from datetime import date

        fee.payment_status = "Paid"
        fee.payment_date = date.today()

        db.session.commit()

        flash(
            "Payment successful!",
            "success"
        )

        return redirect(url_for("student.fees"))

    return render_template(
        "student/pay_fee.html",
        user=current_user,
        fee=fee
    )

# =========================
# STUDENT NOTICES
# =========================

@student.route("/notices")
@login_required
def notices():

    notices = Notice.query.order_by(
        Notice.created_at.desc()
    ).all()

    return render_template(
        "student/notices.html",
        user=current_user,
        notices=notices
    )

@student.route("/notifications/<int:notification_id>/read")
@login_required
def mark_notification_read(notification_id):

    student_profile = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if student_profile is None:
        return "Student profile not found.", 404

    notification = Notification.query.filter_by(
        id=notification_id,
        student_id=student_profile.id
    ).first_or_404()

    notification.is_read = True

    db.session.commit()

    return redirect(url_for("student.notices"))

# =========================
# AI ASSISTANT
# =========================

@student.route("/assistant", methods=["GET", "POST"])
@login_required
def assistant():

    # AI Assistant is for students only
    if current_user.role != "student":
        return "AI Assistant is available for student accounts only.", 403

    student = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    # Safety check if student profile doesn't exist
    if student is None:
        return (
            "Student profile not found. "
            "Please contact the administrator.",
            404
        )

    response = None
    user_message = ""

    if request.method == "POST":

        user_message = request.form.get(
            "message",
            ""
        ).strip()

        if user_message:

            response = get_ai_response(
                student,
                user_message
            )

    return render_template(
        "student/assistant.html",
        user=current_user,
        response=response,
        user_message=user_message
    )