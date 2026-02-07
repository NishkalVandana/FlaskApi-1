import os
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
migrate=Migrate()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    strategy="fixed-window", 
    storage_uri="memory://",
)
