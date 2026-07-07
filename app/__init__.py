from flask import Flask, render_template

from config import Config

from app.extensions import (
    db,
    migrate,
    login_manager,
    mail
)


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)

    mail.init_app(app)

    from app.auth import auth_bp
    from app.weather import weather_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(weather_bp)

    @app.errorhandler(404)
    def page_not_found(error):

        return (
            render_template(
                "errors/404.html"
            ),
            404
        )

    @app.errorhandler(500)
    def internal_error(error):

        db.session.rollback()

        return (
            render_template(
                "errors/500.html"
            ),
            500
        )

    return app