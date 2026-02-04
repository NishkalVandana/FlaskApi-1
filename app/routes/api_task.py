from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import limiter
from app.exceptions import (
    NotFoundError,
    ForbiddenError,
    ValidationError
)

from app.models import Task
from app.extensions import db

api_task = Blueprint("api_task", __name__)


@api_task.route("/api/hello")

def hello():
    return jsonify({"message": "The flask is running"})

# GET all tasks (JWT)

@api_task.route("/api/tasks", methods=["GET"])
@jwt_required()
@limiter.limit("50 per minute")
def get_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

# POST create task (JWT)

@api_task.route("/api/tasks", methods=["POST"])
@jwt_required()
@limiter.limit("50 per minute")
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        raise ValidationError("Request body is required")

    new_task = Task(
        task=data["task"],
        status=False,
        priority=data.get("priority", "Low"),
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201




@api_task.route("/api/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
@limiter.limit("50 per minute")
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        raise ValidationError("Request Body is required")
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        raise NotFoundError("Task not found")

    task.task = data.get("task", task.task)
    task.status = data.get("status", task.status)

    db.session.commit()
    return jsonify(task.to_dict()), 200

# DELETE task (JWT)

@api_task.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
@limiter.limit("50 per minute")
def delete_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        raise NotFoundError("Task not found")

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Successfully deleted"}), 200
