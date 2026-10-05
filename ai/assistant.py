from app.models import (
    Student,
    RoomAllocation,
    Fee,
    Complaint,
    LeaveRequest
)


# =========================================================
# INTENT HELPER
# =========================================================

def contains_any(message, keywords):
    """
    Checks whether any keyword or phrase exists
    as a complete word/phrase in the message.
    """

    message_words = set(message.split())

    for keyword in keywords:

        # Multi-word phrase
        if " " in keyword:

            if keyword in message:
                return True

        # Single word
        else:

            if keyword in message_words:
                return True

    return False


# =========================================================
# AI ASSISTANT
# =========================================================

def get_ai_response(student, message):

    message = message.lower().strip()

    # =====================================================
    # EMPTY MESSAGE
    # =====================================================

    if not message:

        return (
            "Please enter a question. "
            "You can ask me about your room, fees, complaints, "
            "leave requests or profile."
        )


    # =====================================================
    # GREETING
    # =====================================================

    if contains_any(message, [
        "hello",
        "hi",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    ]):

        return (
            f"Hello {student.user.name}! 👋\n\n"
            "I'm Nivasa AI Assistant. "
            "I can help you with your hostel information, "
            "fees, complaints, leave requests and profile."
        )


    # =====================================================
    # HELP
    # =====================================================

    if contains_any(message, [
        "what can you do",
        "what can you help",
        "how can you help",
        "help me",
        "help"
    ]):

        return (
            "I can help you with:\n\n"
            "🏠 Room information\n"
            "💳 Fees and payment status\n"
            "📝 Complaints\n"
            "📅 Leave requests\n"
            "👤 Student profile\n\n"
            "You can ask questions naturally, for example:\n"
            "• Where is my room?\n"
            "• How many beds are available?\n"
            "• Do I have any pending fees?\n"
            "• Show my complaints\n"
            "• What is my leave status?\n"
            "• Show my profile"
        )


    # =====================================================
    # ROOM
    # =====================================================

    if contains_any(message, [
        "my room",
        "room number",
        "which room",
        "where is my room",
        "room details",
        "room information",
        "hostel room",
        "where am i staying",
        "where am i living",
        "my hostel",
        "which hostel",
        "hostel details",
        "room",
        "bed",
        "beds",
        "available beds"
    ]):

        allocation = RoomAllocation.query.filter_by(
            student_id=student.id,
            status="active"
        ).first()


        if not allocation:

            return (
                "You currently do not have an active room allocation."
            )


        room = allocation.room


        return (
            f"🏠 Your room details:\n\n"
            f"Room: {room.room_number}\n"
            f"Hostel: {room.hostel.name}\n"
            f"Floor: {room.floor}\n"
            f"Capacity: {room.capacity} beds\n"
            f"Available beds: {room.available_beds}"
        )


    # =====================================================
    # PENDING FEES
    # =====================================================

    if contains_any(message, [
        "pending fee",
        "pending fees",
        "fee due",
        "fees due",
        "how much do i owe",
        "how much is pending",
        "pending amount",
        "amount pending",
        "fee status",
        "payment status",
        "what do i owe",
        "fees pending"
    ]):

        fees = Fee.query.filter_by(
            student_id=student.id
        ).all()


        pending_fees = [
            fee
            for fee in fees
            if fee.payment_status == "Pending"
        ]


        if not pending_fees:

            return (
                "✅ You currently have no pending fees."
            )


        pending = sum(
            fee.amount
            for fee in pending_fees
        )


        return (
            f"💳 You have {len(pending_fees)} "
            f"pending fee(s).\n\n"
            f"Total pending amount: ₹{pending:.2f}"
        )


    # =====================================================
    # ALL FEES
    # =====================================================

    if contains_any(message, [
        "fee",
        "fees",
        "payment",
        "paid",
        "fee details",
        "fee information",
        "payment details"
    ]):

        fees = Fee.query.filter_by(
            student_id=student.id
        ).all()


        if not fees:

            return (
                "You currently have no fee records."
            )


        total = sum(
            fee.amount
            for fee in fees
        )


        paid = sum(
            fee.amount
            for fee in fees
            if fee.payment_status == "Paid"
        )


        pending = sum(
            fee.amount
            for fee in fees
            if fee.payment_status == "Pending"
        )


        return (
            f"💳 Fee summary:\n\n"
            f"Total fees: ₹{total:.2f}\n"
            f"Paid: ₹{paid:.2f}\n"
            f"Pending: ₹{pending:.2f}"
        )


    # =====================================================
    # COMPLAINT STATUS
    # =====================================================

    if contains_any(message, [
        "complaint status",
        "complaints status",
        "status of my complaint",
        "my complaint status",
        "complaint update",
        "complaint updates",
        "latest complaint",
        "last complaint"
    ]):

        complaints = Complaint.query.filter_by(
            student_id=student.id
        ).order_by(
            Complaint.created_at.desc()
        ).all()


        if not complaints:

            return (
                "You have not submitted any complaints yet."
            )


        latest = complaints[0]


        return (
            f"📝 Your latest complaint:\n\n"
            f"Title: {latest.title}\n"
            f"Category: {latest.category}\n"
            f"Priority: {latest.priority}\n"
            f"Status: {latest.status}"
        )


    # =====================================================
    # COMPLAINT SUMMARY
    # =====================================================

    if contains_any(message, [
        "complaint",
        "complaints",
        "my problems",
        "my issues",
        "hostel problem",
        "hostel issue"
    ]):

        complaints = Complaint.query.filter_by(
            student_id=student.id
        ).order_by(
            Complaint.created_at.desc()
        ).all()


        if not complaints:

            return (
                "You have not submitted any complaints yet."
            )


        unresolved = [
            complaint
            for complaint in complaints
            if complaint.status != "Resolved"
        ]


        if unresolved:

            return (
                f"📝 You have {len(unresolved)} "
                f"unresolved complaint(s).\n\n"
                f"Latest: {unresolved[0].title}\n"
                f"Status: {unresolved[0].status}"
            )


        return (
            f"✅ You have submitted {len(complaints)} "
            "complaint(s), and all of them are resolved."
        )


    # =====================================================
    # LEAVE STATUS
    # =====================================================

    if contains_any(message, [
        "leave status",
        "my leave status",
        "status of my leave",
        "leave request status",
        "leave update",
        "leave updates",
        "latest leave",
        "last leave"
    ]):

        leaves = LeaveRequest.query.filter_by(
            student_id=student.id
        ).order_by(
            LeaveRequest.created_at.desc()
        ).all()


        if not leaves:

            return (
                "You have not submitted any leave requests yet."
            )


        latest = leaves[0]


        return (
            f"📅 Your latest leave request:\n\n"
            f"From: {latest.from_date.strftime('%d %b %Y')}\n"
            f"To: {latest.to_date.strftime('%d %b %Y')}\n"
            f"Status: {latest.status}"
        )


    # =====================================================
    # LEAVE SUMMARY
    # =====================================================

    if contains_any(message, [
        "leave",
        "holiday",
        "permission",
        "leave request",
        "leave requests",
        "my leaves"
    ]):

        leaves = LeaveRequest.query.filter_by(
            student_id=student.id
        ).order_by(
            LeaveRequest.created_at.desc()
        ).all()


        if not leaves:

            return (
                "You have not submitted any leave requests yet. "
                "You can apply for leave from the Leave section."
            )


        pending = [
            leave
            for leave in leaves
            if leave.status == "Pending"
        ]


        approved = [
            leave
            for leave in leaves
            if leave.status == "Approved"
        ]


        rejected = [
            leave
            for leave in leaves
            if leave.status == "Rejected"
        ]


        return (
            f"📅 Leave summary:\n\n"
            f"Total requests: {len(leaves)}\n"
            f"Pending: {len(pending)}\n"
            f"Approved: {len(approved)}\n"
            f"Rejected: {len(rejected)}"
        )


    # =====================================================
    # PROFILE
    # =====================================================

    if contains_any(message, [
        "my profile",
        "profile details",
        "profile information",
        "my name",
        "my enrollment",
        "my course",
        "my branch",
        "student details",
        "student information",
        "who am i"
    ]):

        return (
            f"👤 Your profile:\n\n"
            f"Name: {student.user.name}\n"
            f"Enrollment: "
            f"{student.enrollment_no or 'Not added yet'}\n"
            f"Course: "
            f"{student.course or 'Not added yet'}\n"
            f"Branch: "
            f"{student.branch or 'Not added yet'}\n"
            f"Year: "
            f"{student.year or 'Not added yet'}"
        )


    # =====================================================
    # DEFAULT FALLBACK
    # =====================================================

    return (
        "I'm not sure how to answer that yet. 🤔\n\n"
        "I can help with:\n"
        "🏠 Room\n"
        "💳 Fees\n"
        "📝 Complaints\n"
        "📅 Leave\n"
        "👤 Profile\n\n"
        "Try asking something like:\n"
        "\"Where am I staying?\"\n"
        "\"How many beds are available?\"\n"
        "\"Do I have any pending fees?\"\n"
        "\"Show my complaint status.\""
    )