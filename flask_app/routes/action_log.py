from flask import Blueprint, jsonify

from flask_app.db import get_db
from flask_app.data_queries.action_log import get_all_action_logs
from flask_app.routes.decorators import role_required

action_logs_bp = Blueprint('logs', __name__)


@action_logs_bp.route('/', methods=['GET'])
def list_action_logs():
    conn = get_db()
    action_logs = get_all_action_logs(conn)
    return jsonify(action_logs)