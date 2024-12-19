from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.promotions import (
    create_promotion,
    get_all_promotions,
    get_promotion_by_id,
    update_promotion,
    delete_promotion
)
from flask_app.routes.decorators import role_required

promotions_bp = Blueprint('promotions', __name__)


@promotions_bp.route('/', methods=['GET'])
def list_promotions():
    conn = get_db()
    promotions = get_all_promotions(conn)
    return jsonify(promotions)


@promotions_bp.route('/<uuid:promotion_id>', methods=['GET'])
def get_promotion(promotion_id):
    conn = get_db()
    promotion = get_promotion_by_id(conn, str(promotion_id))
    if promotion is None:
        return jsonify({"error": "promotion not found"}), 404
    return jsonify(promotion)


@promotions_bp.route('/', methods=['POST'])
@role_required(['admin'])
def add_promotion():
    data = request.json
    conn = get_db()
    promotion_id = create_promotion(
        conn,
        data['title'],
        data['description'],
        data['discount'],
        data['end_date'],
        data['service_id']
    )
    return jsonify({"added promotion": promotion_id}), 201


@promotions_bp.route('/<uuid:promotion_id>', methods=['PUT'])
@role_required(['admin'])
def edit_promotion(promotion_id):
    data = request.json
    conn = get_db()
    update_promotion(
        conn,
        str(promotion_id),
        data['title'],
        data['description'],
        data['discount'],
        data['end_date'],
        data['service_id']
    )
    return jsonify({"updated promotion": promotion_id}), 200


@promotions_bp.route('/<uuid:promotion_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_promotion_route(promotion_id):
    conn = get_db()
    delete_promotion(conn, str(promotion_id))
    return jsonify({"deleted promotion": promotion_id}), 200
