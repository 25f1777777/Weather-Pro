from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

import secrets

from app.auth import auth_bp
from app.extensions import db
from app.models import User , SearchHistory 

from app.email_service import (
    send_verification_email,
    verify_token
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("weather.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username"
        ).strip()

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        if not username or not email:
            flash(
                "All fields are required.",
                "danger"
            )
            return redirect(
                url_for("auth.register")
            )

        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "danger"
            )
            return redirect(
                url_for("auth.register")
            )

        existing_user = User.query.filter(
            (User.username == username)
            | (User.email == email)
        ).first()

        if existing_user:
            flash(
                "User already exists.",
                "danger"
            )
            return redirect(
                url_for("auth.register")
            )

        verification_token = (
            secrets.token_urlsafe(32)
        )

        user = User(
            username=username,
            email=email,
            verification_token=verification_token
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        try:

            send_verification_email(
                user.email
            )

            flash(
                "Verification email sent successfully.",
                "success"
            )

        except Exception as e:

            print(e)

            flash(
                "Account created but email could not be sent.",
                "warning"
            )
            
        logout_user() 
        
         
        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )
    

@auth_bp.route("/verify-email/<token>")
def verify_email(token):

    email = verify_token(token)

    if not email:

        flash(
            "Verification link is invalid or has expired.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        flash(
            "User not found.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    if user.is_verified:

        flash(
            "Email already verified.",
            "info"
        )

        return redirect(
            url_for("auth.login")
        )

    user.is_verified = True

    db.session.commit()

    flash(
        "Email verified successfully. You can now login.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )


    
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("weather.dashboard")
        )

    if request.method == "POST":

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            flash(
                "Invalid credentials.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )

        if not user.check_password(
            password
        ):
            flash(
                "Invalid credentials.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )
            
        if not user.is_verified:

            flash(
                "Please verify your email before logging in.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(
            user,
            remember=True
        )

        flash(
            f"Welcome {user.username}!",
            "success"
        )

        return redirect(
            url_for("weather.dashboard")
        )

    return render_template(
        "login.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )



@auth_bp.route("/profile")
@login_required
def profile():

    recent_searches = (
        SearchHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(SearchHistory.searched_at.desc())
        .all()
    )

    return render_template(
        "profile.html",
        recent_searches=recent_searches
    )