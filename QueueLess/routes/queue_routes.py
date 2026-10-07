from flask import Blueprint

queue_bp = Blueprint("queue", __name__)


@queue_bp.route("/")
def queue_index():
    return {"message": "Queue routes placeholder"}
