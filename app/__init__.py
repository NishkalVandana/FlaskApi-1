from flask import Flask
from flask_jwt_extended import JWTManager

from app.extensions import db, limiter
from app.errors import register_error_handlers


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret_key"
    app.config["JWT_SECRET_KEY"] = "super_secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    jwt = JWTManager()
    jwt.init_app(app)
    db.init_app(app)
    limiter.init_app(app)

    # 🔥 IMPORT BLUEPRINTS ONLY AFTER limiter.init_app
    from app.routes.api_auth import api_auth
    from app.routes.api_task import api_task

    app.register_blueprint(api_auth)
    app.register_blueprint(api_task)

    register_error_handlers(app)

    return app
