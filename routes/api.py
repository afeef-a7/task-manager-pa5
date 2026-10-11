from flask import Blueprint, Response, jsonify, request

from services.products import create_product
from services.tasks import (
    create_task,
    get_task,
    get_tasks,
    parse_priority,
    update_task_priority,
)
from services.users import (
    get_notification_pref,
    get_user,
    get_users,
    update_notification_pref,
)
from utils.errors import AppError, ValidationError

api = Blueprint("api", __name__)

@api.errorhandler(AppError)
def handle_app_error(e):
    return jsonify({"error": e.message}), e.status_code

@api.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_route(task_id):
    return jsonify(get_task(task_id))

@api.route("/tasks", methods=["GET"])
def list_tasks_route() -> Response:
    priority = request.args.get("priority")
    if priority is None:
        return jsonify(get_tasks())
    return jsonify(get_tasks(parse_priority(priority)))

@api.route("/tasks", methods=["POST"])
def create_task_route():
    data = request.get_json()
    return jsonify(create_task(data["title"], data["user_id"], data.get("priority", 3))), 201

@api.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task_route(task_id: int) -> Response:
    data = request.get_json(silent=True) or {}
    return jsonify(update_task_priority(task_id, data.get("priority")))

@api.route("/users", methods=["GET"])
def list_users_route() -> Response:
    """List all users.

    Returns:
        A JSON list of user records, each including notification_pref.
    """
    return jsonify(get_users())

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    return jsonify(get_user(user_id))

@api.route("/users/<int:user_id>/notifications", methods=["GET"])
def get_notifications_route(user_id: int) -> Response:
    """Get a user's notification preference.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        A JSON object with the user's ID and notification_pref.

    Raises:
        NotFoundError: If no user exists with the given ID.
    """
    return jsonify({"user_id": user_id, "notification_pref": get_notification_pref(user_id)})

@api.route("/users/<int:user_id>/notifications", methods=["PATCH"])
def update_notifications_route(user_id: int) -> Response:
    """Update a user's notification preference.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        A JSON object with the user's ID and updated notification_pref.

    Raises:
        NotFoundError: If no user exists with the given ID.
        ValidationError: If notification_pref is missing or not one of the
            allowed values.
    """
    data = request.get_json(silent=True) or {}
    pref = data.get("notification_pref")
    if not isinstance(pref, str):
        raise ValidationError("notification_pref", "must be one of: email, sms, none")
    user = update_notification_pref(user_id, pref)
    return jsonify({"user_id": user["id"], "notification_pref": user["notification_pref"]})

@api.route("/products", methods=["POST"])
def create_product_route():
    data = request.get_json()
    return jsonify(create_product(data["name"], data["price"])), 201
