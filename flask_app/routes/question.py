from flask import Blueprint, jsonify, request

from flask_app.db import get_db
from flask_app.data_queries.question import (get_all_questions,
                                   get_question_by_id,
                                   create_question,
                                   remove_question,
                                   update_question,
                                   answer_asked_question)
from flask_app.routes.decorators import role_required

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['GET'])
def list_questions():
    conn = get_db()
    questions = get_all_questions(conn)
    return jsonify(questions)


@questions_bp.route('/<uuid:question_id>', methods=['GET'])
def get_question(question_id):
    conn = get_db()
    question = get_question_by_id(conn, str(question_id))
    if question is None:
        return jsonify({"error": "question not found"}), 404
    return jsonify(question)


@questions_bp.route('/', methods=['POST'])
@role_required(['admin', 'passenger'])
def add_question():
    data = request.json
    conn = get_db()

    question_id = create_question(
        conn,
        data['user_id'],
        data['question'],
    )

    return jsonify({"added question": question_id}), 201


@questions_bp.route('/delete/<uuid:question_id>', methods=['DELETE'])
@role_required(['admin', 'passenger'])
def delete_question(question_id):
    conn = get_db()
    remove_question(conn, str(question_id))
    return jsonify({"deleted: uuid": question_id}), 201


@questions_bp.route('/edit/<uuid:question_id>', methods=['PUT'])
@role_required(['admin', 'passenger'])
def edit_question(question_id):
    data = request.json
    conn = get_db()
    update_question(
        conn,
        str(question_id),
        data['user_id'],
        data['question'],
    )
    return jsonify({"updated question: uuid": question_id}), 201


@questions_bp.route('/answer/<uuid:question_id>', methods=['PUT'])
@role_required(['admin'])
def answer_question(question_id):
    data = request.json
    conn = get_db()
    answer_asked_question(
        conn,
        str(question_id),
        data['answer']
    )
    return jsonify({"answered question: uuid": question_id}), 201