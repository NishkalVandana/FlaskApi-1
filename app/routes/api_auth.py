from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from app.extensions import db, limiter
from app.models import User, TokenBlacklist

api_auth = Blueprint("api_auth", __name__)

#  REGISTER 
@api_auth.route("/api/register", methods=["POST"])
@limiter.limit("2/minute")
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "username, email, password required"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "User already exists"}, 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"msg": "User registered successfully"}, 201


#  LOGIN 
@api_auth.route("/api/login", methods=["POST"])
@limiter.limit("10/hour")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=5)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, 200


#  REFRESH 
@api_auth.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]

    if TokenBlacklist.query.filter_by(jti=jti).first():
        return {"msg": "Token revoked"}, 401

    user_id = get_jwt_identity()

    new_access_token = create_access_token(
        identity=str(user_id),
        expires_delta=timedelta(seconds=30)
    )

    return {"access_token": new_access_token}, 200


#  LOGOUT 
@api_auth.route("/api/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]

    if TokenBlacklist.query.filter_by(jti=jti).first():
        return {"msg": "Already logged out"}, 400

    db.session.add(TokenBlacklist(jti=jti))
    db.session.commit()

    return {"msg": "Logged out successfully"}, 200
