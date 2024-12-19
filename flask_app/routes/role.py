from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.role import (
    create_role,
    get_all_roles,
    get_role_by_id,
    update_role,
    delete_role
)
from flask_app.routes.decorators import role_required

roles_bp = Blueprint('roles', __name__)


@roles_bp.route('/', methods=['GET'])
def list_roles():
    conn = get_db()
    roles = get_all_roles(conn)
    return jsonify(roles)


@roles_bp.route('/<uuid:role_id>', methods=['GET'])
def get_role(role_id):
    conn = get_db()
    role = get_role_by_id(conn, str(role_id))
    if role is None:
        return jsonify({"error": "role not found"}), 404
    return jsonify(role)


@roles_bp.route('/', methods=['POST'])
@role_required(['admin'])
def add_role():
    data = request.json
    conn = get_db()
    role_id = create_role(
        conn,
        data['name']
    )
    return jsonify({"added role": role_id}), 201


@roles_bp.route('/<uuid:role_id>', methods=['PUT'])
@role_required(['admin'])
def edit_role(role_id):
    data = request.json
    conn = get_db()
    update_role(
        conn,
        str(role_id),
        data['name']
    )
    return jsonify({"updated role": role_id}), 200


@roles_bp.route('/<uuid:role_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_role_route(role_id):
    conn = get_db()
    delete_role(conn, str(role_id))
    return jsonify({"deleted role": role_id}), 200
