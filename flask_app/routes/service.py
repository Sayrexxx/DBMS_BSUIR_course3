from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.service import (
    create_service,
    get_all_services,
    get_service_by_id,
    update_service,
    delete_service
)
from flask_app.routes.decorators import role_required

services_bp = Blueprint('services', __name__)


@services_bp.route('/', methods=['GET'])
def list_services():
    conn = get_db()
    services = get_all_services(conn)
    return jsonify(services)


@services_bp.route('/<uuid:service_id>', methods=['GET'])
def get_service(service_id):
    conn = get_db()
    service = get_service_by_id(conn, str(service_id))
    if service is None:
        return jsonify({"error": "service not found"}), 404
    return jsonify(service)


@services_bp.route('/', methods=['POST'])
@role_required(['admin'])
def add_service():
    data = request.json
    conn = get_db()
    service_id = create_service(
        conn,
        data['myuser_id'],
        data['name'],
        data['price']
    )
    return jsonify({"added service": service_id}), 201


@services_bp.route('/<uuid:service_id>', methods=['PUT'])
@role_required(['admin'])
def edit_service(service_id):
    data = request.json
    conn = get_db()
    update_service(
        conn,
        str(service_id),
        data['myuser_id'],
        data['name'],
        data['price']
    )
    return jsonify({"updated service": service_id}), 200


@services_bp.route('/<uuid:service_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_service_route(service_id):
    conn = get_db()
    delete_service(conn, str(service_id))
    return jsonify({"deleted service": service_id}), 200
