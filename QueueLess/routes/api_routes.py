from flask import Blueprint, jsonify, request

from models import token as token_model
from models import appointment as appointment_model

api_bp = Blueprint("api", __name__)


@api_bp.route("/queue/<int:token_id>")
def queue_status_api(token_id):
    queue_status = token_model.get_queue_status_for_token(token_id)
    if not queue_status:
        return jsonify({"error": "Token not found"}), 404

    return jsonify(queue_status)


@api_bp.route("/slots")
def get_slots():
    service_id = request.args.get("service_id", type=int)
    date_str = request.args.get("date")
    
    if not service_id or not date_str:
        return jsonify({"status": "error", "message": "Missing parameters", "slots": []}), 400
        
    slots = appointment_model.get_available_slots(service_id, date_str)
    return jsonify({"status": "success", "slots": slots})


@api_bp.route("/notifications/unread-count")
def unread_count():
    from utils.auth import session
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"unread_count": 0}), 401
    
    from models import notifications as notif_model
    count = notif_model.get_unread_count(user_id)
    return jsonify({"unread_count": count})


@api_bp.route("/admin/chart-data")
def admin_chart_data():
    from utils.auth import session
    if not session.get("logged_in") or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    from models import admin as admin_model
    data = admin_model.get_all_charts_data()
    return jsonify({"status": "success", "data": data})

