from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.flight import (
    create_flight,
    get_all_flights,
    get_flight_by_id,
    update_flight,
    delete_flight
)
from flask_app.routes.decorators import role_required

flights_bp = Blueprint('flights', __name__)


@flights_bp.route('/', methods=['GET'])
def list_flights():
    conn = get_db()
    flights = get_all_flights(conn)
    return jsonify(flights)


@flights_bp.route('/<uuid:flight_id>', methods=['GET'])
def get_flight(flight_id):
    conn = get_db()
    flight = get_flight_by_id(conn, str(flight_id))
    if flight is None:
        return jsonify({"error": "flight not found"}), 404
    return jsonify(flight)


@flights_bp.route('/', methods=['POST'])
@role_required(['admin'])
def add_flight():
    data = request.json
    conn = get_db()
    flight_id = create_flight(
        conn,
        data['service_id'],
        data['origin_point'],
        data['destination_point'],
        data['departure_datetime'],
        data['arrival_datetime'],
        data['price'],
        data['plane_id']
    )
    return jsonify({"added flight": flight_id}), 201


@flights_bp.route('/<uuid:flight_id>', methods=['PUT'])
@role_required(['admin'])
def edit_flight(flight_id):
    data = request.json
    conn = get_db()
    update_flight(
        conn,
        str(flight_id),
        data['service_id'],
        data['origin_point'],
        data['destination_point'],
        data['departure_datetime'],
        data['arrival_datetime'],
        data['price'],
        data['plane_id']
    )
    return jsonify({"updated flight": flight_id}), 200


@flights_bp.route('/<uuid:flight_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_flight_route(flight_id):
    conn = get_db()
    delete_flight(conn, str(flight_id))
    return jsonify({"deleted flight": flight_id}), 200
