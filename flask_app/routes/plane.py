from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.plane import (
    create_plane,
    get_all_planes,
    get_plane_by_id,
    update_plane,
    delete_plane
)
from flask_app.routes.decorators import role_required

planes_bp = Blueprint('planes', __name__)


@planes_bp.route('/', methods=['GET'])
def list_planes():
    conn = get_db()
    planes = get_all_planes(conn)
    return jsonify(planes)


@planes_bp.route('/<uuid:plane_id>', methods=['GET'])
def get_plane(plane_id):
    conn = get_db()
    plane = get_plane_by_id(conn, str(plane_id))
    if plane is None:
        return jsonify({"error": "plane not found"}), 404
    return jsonify(plane)


@planes_bp.route('/', methods=['POST'])
@role_required(['admin'])
def add_plane():
    data = request.json
    conn = get_db()
    plane_id = create_plane(
        conn,
        data['available_seats'],
        data['model'],
        data['company']
    )
    return jsonify({"added plane": plane_id}), 201


@planes_bp.route('/<uuid:plane_id>', methods=['PUT'])
@role_required(['admin'])
def edit_plane(plane_id):
    data = request.json
    conn = get_db()
    update_plane(
        conn,
        str(plane_id),
        data['available_seats'],
        data['model'],
        data['company']
    )
    return jsonify({"updated plane": plane_id}), 200


@planes_bp.route('/<uuid:plane_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_plane_route(plane_id):
    conn = get_db()
    delete_plane(conn, str(plane_id))
    return jsonify({"deleted plane": plane_id}), 200
