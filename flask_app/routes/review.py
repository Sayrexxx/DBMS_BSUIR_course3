from flask import Blueprint, jsonify, request
from flask_app.db import get_db
from flask_app.data_queries.review import (
    create_review,
    get_all_reviews,
    get_review_by_id,
    update_review,
    delete_review
)
from flask_app.routes.decorators import role_required

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/', methods=['GET'])
def list_reviews():
    conn = get_db()
    reviews = get_all_reviews(conn)
    return jsonify(reviews)


@reviews_bp.route('/<uuid:review_id>', methods=['GET'])
def get_review(review_id):
    conn = get_db()
    review = get_review_by_id(conn, str(review_id))
    if review is None:
        return jsonify({"error": "review not found"}), 404
    return jsonify(review)


@reviews_bp.route('/', methods=['POST'])
@role_required(['admin', 'passenger'])
def add_review():
    data = request.json
    conn = get_db()
    review_id = create_review(
        conn,
        data['text'],
        data['grade'],
        data['myuser_id']
    )
    return jsonify({"added review": review_id}), 201


@reviews_bp.route('/<uuid:review_id>', methods=['PUT'])
@role_required(['admin', 'employee', 'customer'])
def edit_review(review_id):
    data = request.json
    conn = get_db()
    update_review(
        conn,
        str(review_id),
        data['text'],
        data['grade'],
    )
    return jsonify({"updated review": review_id}), 200


@reviews_bp.route('/<uuid:review_id>', methods=['DELETE'])
@role_required(['admin', 'passenger'])
def delete_review_route(review_id):
    conn = get_db()
    delete_review(conn, str(review_id))
    return jsonify({"deleted review": review_id}), 200
