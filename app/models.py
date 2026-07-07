from datetime import datetime

from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import (
    db,
    login_manager
)


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )


class User(
    UserMixin,
    db.Model
):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    is_active_user = db.Column(
        db.Boolean,
        default=True
    )
    
    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    verification_token = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )

    favorites = db.relationship(
        "FavoriteCity",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    searches = db.relationship(
        "SearchHistory",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(
        self,
        password
    ):

        self.password_hash = (
            generate_password_hash(
                password
            )
        )

    def check_password(
        self,
        password
    ):

        return (
            check_password_hash(
                self.password_hash,
                password
            )
        )


    def __repr__(self):

        return (
            f"<User {self.username}>"
        )



class FavoriteCity(
    db.Model
):

    __tablename__ = (
        "favorite_cities"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    city_name = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    __table_args__ = (

        db.UniqueConstraint(
            "user_id",
            "city_name",
            name="unique_user_city"
        ),

    )

    def __repr__(self):

        return (
            f"<FavoriteCity "
            f"{self.city_name}>"
        )


class SearchHistory(db.Model):

    __tablename__ = "search_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    city_name = db.Column(
        db.String(100),
        nullable=False
    )

    temperature = db.Column(
        db.Float,
        nullable=True
    )

    weather_condition = db.Column(
        db.String(100),
        nullable=True
    )

    searched_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )