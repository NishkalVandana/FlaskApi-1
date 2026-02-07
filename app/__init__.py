import os
from flask import Flask
from app.extensions import db, limiter
from app.errors import register_error_handlers
from app.extensions import migrate
from app.extensions import jwt
def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["RATELIMIT_ENABLED"] = False
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    jwt.init_app(app)

    from app.routes.api_auth import api_auth
    from app.routes.api_task import api_task
    app.register_blueprint(api_auth)
    app.register_blueprint(api_task)
    register_error_handlers(app)
    limiter.init_app(app)
    return app
