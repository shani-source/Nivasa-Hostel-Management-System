from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.extensions import db
from app.models import User


auth = Blueprint(
    "auth",
    __name__,
    url_prefix=""
)


# ================= LOGIN =================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(password):

            login_user(user)

            flash(
                "Login successful!",
                "success"
            )

            # Admin → Admin Dashboard
            if user.role == "admin":
                return redirect(
                    url_for("admin.dashboard")
                )

            # Student → Student Dashboard
            if user.role == "student":
                return redirect(
                    url_for("student.dashboard")
                )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "auth/login.html"
    )


# ================= LOGOUT =================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("index")
    )


# ================= ADMIN LOGIN =================

@auth.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        # Only admin accounts can use this login
        if user and user.check_password(password):

            if user.role == "admin":

                login_user(user)

                flash(
                    "Admin login successful!",
                    "success"
                )

                return redirect(
                    url_for("admin.dashboard")
                )

            flash(
                "Only administrators can use this login.",
                "error"
            )

        else:

            flash(
                "Invalid admin email or password.",
                "error"
            )

    return render_template(
        "auth/admin_login.html"
    )

# ================= PUBLIC REGISTRATION DISABLED =================

@auth.route("/register", methods=["GET", "POST"])
def register():

    return (
        url_for("auth.admin_login")
    )