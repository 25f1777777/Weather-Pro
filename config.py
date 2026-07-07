import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )
    
    API_KEY = os.getenv(
        "API_KEY"
    )


    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///weather.db"
    )
    
    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY"
    )
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = (DATABASE_URL)

    SQLALCHEMY_TRACK_MODIFICATIONS = ( False)
    
    

    SESSION_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = False

    REMEMBER_COOKIE_SECURE = False
    
    
    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_USERNAME"
    )


    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    MAX_CONTENT_LENGTH = (
        5 * 1024 * 1024
    )

    SEARCH_HISTORY_LIMIT = 10