from flask import (
    current_app,
    render_template
)

from flask_mail import (
    Message
)

from app.extensions import (
    mail
)

from itsdangerous import (
    URLSafeTimedSerializer
)


def generate_verification_token(email):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt="email-verification"
    )


def verify_token(
    token,
    expiration=3600
):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="email-verification",
            max_age=expiration
        )

        return email

    except Exception:

        return None


def send_verification_email(
    user_email
):

    token = generate_verification_token(
        user_email
    )

    activation_link = (
        f"http://127.0.0.1:5000"
        f"/verify-email/{token}"
    )

    html_content = render_template(
        "emails/verification_email.html",
        activation_link=activation_link
    )

    msg = Message(

        subject=
        "Verify Your WeatherPro Account",

        recipients=[
            user_email
        ],

        html=
        html_content

    )

    mail.send(msg)

    return token