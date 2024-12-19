from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.booking import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    update_booking,
    delete_booking
)
from flask_app.routes.decorators import role_required

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/', methods=['GET'])
def list_bookings():
    conn = get_db()
    bookings = get_all_bookings(conn)
    return jsonify(bookings)


@bookings_bp.route('/<uuid:booking_id>', methods=['GET'])
def get_booking(booking_id):
    conn = get_db()
    booking = get_booking_by_id(conn, str(booking_id))
    if booking is None:
        return jsonify({"error": "booking not found"}), 404
    return jsonify(booking)


@bookings_bp.route('/', methods=['POST'])
@role_required(['admin'])
def add_booking():
    data = request.json
    conn = get_db()
    booking_id = create_booking(
        conn,
        data['flight_id'],
        data['myuser_id'],
        data['seats_amount'],
        data['price']
    )
    return jsonify({"added booking": booking_id}), 201


@bookings_bp.route('/<uuid:booking_id>', methods=['PUT'])
@role_required(['admin'])
def edit_booking(booking_id):
    data = request.json
    conn = get_db()
    update_booking(
        conn,
        str(booking_id),
        data['seats_amount'],
        data['price']
    )
    return jsonify({"updated booking": booking_id}), 200


@bookings_bp.route('/<uuid:booking_id>', methods=['DELETE'])
@role_required(['admin', 'employee'])
def delete_booking_route(booking_id):
    conn = get_db()
    delete_booking(conn, str(booking_id))
    return jsonify({"deleted booking": booking_id}), 200
