from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.myuser_service import (add_service_to_user_query,
                                                  remove_service_from_user_query,
                                                  get_services_by_user,
                                                  get_users_by_service)
from flask_app.routes.decorators import role_required

myuser_service_bp = Blueprint('myuser_service', __name__)

@myuser_service_bp.route('/add', methods=['POST'])
@role_required(['admin'])
def add_service_to_user():
    data = request.json
    conn = get_db()

    try:
        service_id = add_service_to_user_query(conn, data['myuser_id'], data['service_id'])
        return jsonify({"added_service_id": service_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@myuser_service_bp.route('/remove', methods=['DELETE'])
@role_required(['admin', 'employee'])
def remove_service_from_user():
    data = request.json
    conn = get_db()

    try:
        success = remove_service_from_user_query(conn, data['myuser_service_id'])
        if success:
            return jsonify({"message": "Service removed successfully"}), 200
        else:
            return jsonify({"error": "Failed to remove service"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@myuser_service_bp.route('/user/<uuid:myuser_id>', methods=['GET'])
def get_services_for_user(myuser_id):
    conn = get_db()

    try:
        services = get_services_by_user(conn, str(myuser_id))
        return jsonify(services), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@myuser_service_bp.route('/service/<uuid:service_id>', methods=['GET'])
def get_users_for_service(service_id):
    conn = get_db()

    try:
        users = get_users_by_service(conn, str(service_id))
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
