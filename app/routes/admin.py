from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import User, Hostel, Room , Student , RoomAllocation , Complaint , LeaveRequest , Fee , Notice , Notification


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)
@admin.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        return "Access denied", 403

    hostels = Hostel.query.all()
    rooms = Room.query.all()
    students = Student.query.all()
    complaints = Complaint.query.all()

    return render_template(
        "admin/dashboard.html",
        user=current_user,
        hostels=hostels,
        rooms=rooms,
        students=students,
        complaints=complaints
    )
# ================= HOSTEL VIEW =================

@admin.route("/hostels")
@login_required
def hostels():

    if current_user.role != "admin":
        return "Access denied", 403

    hostels = Hostel.query.all()
    rooms = Room.query.all()
    allocations = RoomAllocation.query.filter_by(
        status="active"
    ).all()

    return render_template(
        "admin/hostels.html",
        user=current_user,
        hostels=hostels,
        rooms=rooms,
        allocations=allocations
    )


# ================= ADD STUDENT =================

@admin.route(
    "/students/create",
    methods=["GET", "POST"]
)
@login_required
def create_student():

    # Admin only
    print(
        "CREATE STUDENT:",
        current_user.is_authenticated,
        current_user.email,
        current_user.role
    )

    if current_user.role != "admin":
       return "Access denied", 403

    if request.method == "POST":

        # ================= USER DETAILS =================

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        # ================= STUDENT DETAILS =================

        enrollment_no = request.form.get(
            "enrollment_no",
            ""
        ).strip()

        course = request.form.get(
            "course",
            ""
        ).strip()

        branch = request.form.get(
            "branch",
            ""
        ).strip()

        year = request.form.get(
            "year",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        # ================= VALIDATION =================

        if not name or not email or not password:
            flash(
                "Name, email and password are required.",
                "error"
            )
            return redirect(
                url_for("admin.create_student")
            )

        if len(password) < 6:
            flash(
                "Password must contain at least 6 characters.",
                "error"
            )
            return redirect(
                url_for("admin.create_student")
            )

        # ================= CHECK EMAIL =================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash(
                "A user with this email already exists.",
                "error"
            )
            return redirect(
                url_for("admin.create_student")
            )

        # ================= CHECK ENROLLMENT =================

        if enrollment_no:

            existing_student = Student.query.filter_by(
                enrollment_no=enrollment_no
            ).first()

            if existing_student:
                flash(
                    "This enrollment number already exists.",
                    "error"
                )
                return redirect(
                    url_for("admin.create_student")
                )

        # ================= CREATE USER + STUDENT =================

        try:

            user = User(
                name=name,
                email=email,
                role="student"
            )

            user.set_password(password)

            db.session.add(user)
            db.session.flush()

            student = Student(
                user_id=user.id,
                enrollment_no=enrollment_no or None,
                course=course or None,
                branch=branch or None,
                year=int(year) if year else None,
                gender=gender or None,
                phone=phone or None,
                address=address or None
            )

            db.session.add(student)
            db.session.commit()

            flash(
                "Student account created successfully.",
                "success"
            )

            return redirect(
                url_for("admin.students")
            )

        except Exception as e:

            db.session.rollback()

            print(
                "CREATE STUDENT ERROR:",
                e
            )

            flash(
                "Unable to create student account.",
                "error"
            )

            return redirect(
                url_for("admin.create_student")
            )

    return render_template(
        "admin/create_student.html",
        user=current_user
    )



# ================= ROOM VIEW =================

@admin.route("/rooms")
@login_required
def rooms():

    if current_user.role != "admin":
        return "Access denied", 403

    hostel_id = request.args.get("hostel_id", type=int)

    if hostel_id:
        hostel = Hostel.query.get_or_404(hostel_id)

        rooms = Room.query.filter_by(
            hostel_id=hostel_id
        ).all()

        allocations = RoomAllocation.query.filter(
            RoomAllocation.status == "active",
            RoomAllocation.room_id.in_(
                [room.id for room in rooms]
            )
        ).all()

    else:
        hostel = None

        rooms = Room.query.all()

        allocations = RoomAllocation.query.filter_by(
            status="active"
        ).all()

    return render_template(
        "admin/rooms.html",
        user=current_user,
        rooms=rooms,
        allocations=allocations,
        hostel=hostel
    )


# ================= STUDENT VIEW =================
# ================= STUDENT VIEW =================

@admin.route("/students")
@login_required
def students():

    if current_user.role != "admin":
        return "Access denied", 403

    selected_course = request.args.get(
        "course",
        ""
    ).strip()

    # All courses
    courses = db.session.query(
        Student.course
    ).filter(
        Student.course.isnot(None)
    ).filter(
        Student.course != ""
    ).distinct().order_by(
        Student.course
    ).all()

    courses = [
        item[0]
        for item in courses
    ]

    # Course counts
    course_counts = {}

    for course_name in courses:
        course_counts[course_name] = Student.query.filter_by(
            course=course_name
        ).count()

    # Students
    if selected_course:
        students = Student.query.filter_by(
            course=selected_course
        ).order_by(
            Student.enrollment_no
        ).all()
    else:
        students = Student.query.order_by(
            Student.course,
            Student.enrollment_no
        ).all()

    # Active room allocations
    allocations = RoomAllocation.query.filter_by(
        status="active"
    ).all()

    return render_template(
        "admin/students.html",
        user=current_user,
        students=students,
        allocations=allocations,
        courses=courses,
        course_counts=course_counts,
        selected_course=selected_course,
        total_students=Student.query.count()
    )


@admin.route("/hostels/create", methods=["GET", "POST"])
@login_required
def create_hostel():

    if current_user.role != "admin":
        return "Access denied", 403

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        warden_name = request.form.get("warden_name", "").strip()
        gender = request.form.get("gender", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            flash("Hostel name is required.", "error")
            return redirect(url_for("admin.create_hostel"))

        hostel = Hostel(
            name=name,
            warden_name=warden_name,
            gender=gender,
            address=address
        )

        db.session.add(hostel)
        db.session.commit()

        flash("Hostel created successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/create_hostel.html")
@admin.route("/rooms/create", methods=["GET", "POST"])
@login_required
def create_room():

    if current_user.role != "admin":
        return "Access denied", 403

    hostels = Hostel.query.all()

    if request.method == "POST":

        hostel_id = request.form.get("hostel_id")
        room_number = request.form.get("room_number", "").strip()
        floor = request.form.get("floor", "").strip()
        capacity = request.form.get("capacity", "").strip()

        if not hostel_id or not room_number or not capacity:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("admin.create_room"))

        room = Room(
            hostel_id=int(hostel_id),
            room_number=room_number,
            floor=int(floor) if floor else None,
            capacity=int(capacity),
            occupied=0,
            status="available"
        )

        db.session.add(room)
        db.session.commit()

        flash("Room created successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/create_room.html",
        hostels=hostels
    )
# ================= ROOM ALLOCATION =================

@admin.route("/allocations/create", methods=["GET", "POST"])
@login_required
def create_allocation():

    if current_user.role != "admin":
        return "Access denied", 403

    students = Student.query.all()
    rooms = Room.query.all()

    if request.method == "POST":

        student_id = request.form.get("student_id")
        room_id = request.form.get("room_id")

        if not student_id or not room_id:
            flash(
                "Please select both student and room.",
                "error"
            )
            return redirect(
                url_for("admin.create_allocation")
            )

        student = Student.query.get(int(student_id))
        room = Room.query.get(int(room_id))

        if not student or not room:
            flash(
                "Invalid student or room.",
                "error"
            )
            return redirect(
                url_for("admin.create_allocation")
            )

        # Check existing active allocation
        existing = RoomAllocation.query.filter_by(
            student_id=student.id,
            status="active"
        ).first()

        if existing:
            flash(
                "This student already has a room.",
                "error"
            )
            return redirect(
                url_for("admin.create_allocation")
            )

        # Check room capacity
        if room.occupied >= room.capacity:
            flash(
                "This room is already full.",
                "error"
            )
            return redirect(
                url_for("admin.create_allocation")
            )

        allocation = RoomAllocation(
            student_id=student.id,
            room_id=room.id,
            status="active"
        )

        room.occupied += 1

        if room.occupied >= room.capacity:
            room.status = "full"
        else:
            room.status = "available"

        db.session.add(allocation)
        db.session.commit()

        flash(
            "Room allocated successfully!",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    return render_template(
        "admin/create_allocation.html",
        students=students,
        rooms=rooms
    )
# ================= COMPLAINT MANAGEMENT =================

@admin.route("/complaints")
@login_required
def complaints():

    if current_user.role != "admin":
        return "Access denied", 403

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        "admin/complaints.html",
        user=current_user,
        complaints=complaints
    )


@admin.route("/complaints/<int:complaint_id>/status",
             methods=["POST"])
@login_required
def update_complaint_status(complaint_id):

    if current_user.role != "admin":
        return "Access denied", 403

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    new_status = request.form.get(
        "status",
        "Pending"
    )

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:

        flash(
            "Invalid complaint status.",
            "error"
        )

        return redirect(
            url_for("admin.complaints")
        )

    complaint.status = new_status

    db.session.commit()

    flash(
        "Complaint status updated.",
        "success"
    )

    return redirect(
        url_for("admin.complaints")
    )
# ================= LEAVE MANAGEMENT =================

@admin.route("/leave")
@login_required
def leave_requests():

    if current_user.role != "admin":
        return "Access denied", 403

    leave_requests = LeaveRequest.query.order_by(
        LeaveRequest.created_at.desc()
    ).all()

    return render_template(
        "admin/leave.html",
        user=current_user,
        leave_requests=leave_requests
    )


@admin.route("/leave/<int:leave_id>/status",
             methods=["POST"])
@login_required
def update_leave_status(leave_id):

    if current_user.role != "admin":
        return "Access denied", 403

    leave_request = LeaveRequest.query.get_or_404(
        leave_id
    )

    new_status = request.form.get(
        "status",
        "Pending"
    )

    remark = request.form.get(
        "admin_remark",
        ""
    ).strip()

    allowed_statuses = [
        "Pending",
        "Approved",
        "Rejected"
    ]

    if new_status not in allowed_statuses:

        flash(
            "Invalid leave status.",
            "error"
        )

        return redirect(
            url_for("admin.leave_requests")
        )

    leave_request.status = new_status
    leave_request.admin_remark = remark

    db.session.commit()

    flash(
        "Leave request updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin.leave_requests")
    )
# =========================
# FEES MANAGEMENT
# =========================

@admin.route("/fees")
@login_required
def fees():

    if current_user.role != "admin":
        return "Access denied", 403

    fees = Fee.query.order_by(
        Fee.due_date.desc()
    ).all()

    students = Student.query.all()

    return render_template(
        "admin/fees.html",
        fees=fees,
        students=students
    )


@admin.route("/fees/create", methods=["GET", "POST"])
@login_required
def create_fee():

    if current_user.role != "admin":
        return "Access denied", 403

    students = Student.query.all()

    if request.method == "POST":

        student_id = request.form.get("student_id")
        amount = request.form.get("amount")
        fee_type = request.form.get("fee_type")
        due_date = request.form.get("due_date")

        if not student_id or not amount or not fee_type or not due_date:

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for("admin.create_fee")
            )

        try:

            from datetime import datetime

            fee = Fee(
                student_id=int(student_id),
                amount=float(amount),
                fee_type=fee_type,
                due_date=datetime.strptime(
                    due_date,
                    "%Y-%m-%d"
                ).date(),
                payment_status="Pending"
            )

            db.session.add(fee)
            db.session.commit()

            flash(
                "Fee record created successfully.",
                "success"
            )

            return redirect(
                url_for("admin.fees")
            )

        except Exception as e:

            db.session.rollback()

            print("FEE ERROR:", e)

            flash(
                "Unable to create fee record.",
                "error"
            )

            return redirect(
                url_for("admin.create_fee")
            )

    # IMPORTANT:
    # This handles the GET request.

    return render_template(
        "admin/create_fee.html",
        students=students
    )


@admin.route("/fees/<int:fee_id>/status", methods=["POST"])
@login_required
def update_fee_status(fee_id):

    if current_user.role != "admin":
        return "Access denied", 403

    from datetime import date

    fee = Fee.query.get_or_404(fee_id)

    status = request.form.get("status")

    if status not in ["Paid", "Pending"]:
        flash("Invalid payment status.", "error")

        return redirect(
            url_for("admin.fees")
        )

    fee.payment_status = status

    if status == "Paid":
        fee.payment_date = date.today()

    else:
        fee.payment_date = None

    db.session.commit()

    flash(
        "Payment status updated.",
        "success"
    )

    return redirect(
        url_for("admin.fees")
    )
# =========================
# NOTICE MANAGEMENT
# =========================

@admin.route("/notices")
@login_required
def notices():

    if current_user.role != "admin":
        return "Access denied", 403

    notices = Notice.query.order_by(
        Notice.created_at.desc()
    ).all()

    return render_template(
        "admin/notices.html",
        notices=notices
    )


@admin.route("/notices/create", methods=["GET", "POST"])
@login_required
def create_notice():

    if current_user.role != "admin":
        return "Access denied", 403

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category")

        if not title or not content or not category:

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for("admin.create_notice")
            )
        notice = Notice(
            title=title.strip(),
            content=content.strip(),
            category=category
        )

        db.session.add(notice)

        # Get the notice ID before creating notifications
        db.session.flush()

        # Create notification for every student
        students = Student.query.all()

        for student in students:

               notification = Notification(
                   student_id=student.id,
                   notice_id=notice.id,
                   title=notice.title,
                   message=notice.content,
                   category=notice.category
               )

        db.session.add(notification)

        db.session.commit()

        flash(
             "Notice published successfully.",
              "success"
        )
        

        return redirect(
            url_for("admin.notices")
        )

    return render_template(
        "admin/create_notice.html"
    )


@admin.route("/notices/<int:notice_id>/delete", methods=["POST"])
@login_required
def delete_notice(notice_id):

    if current_user.role != "admin":
        return "Access denied", 403

    notice = Notice.query.get_or_404(notice_id)

    db.session.delete(notice)
    db.session.commit()

    flash(
        "Notice deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.notices")
    )