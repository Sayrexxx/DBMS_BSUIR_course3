import datetime

from flask import Blueprint, jsonify, request
import jwt

from flask_app.db import get_db
from flask_app.data_queries.myuser import (
    create_user,
    get_user_by_nickname_query,
    get_user_by_id_query,
    get_all_users,
    update_user_role
)
from flask_app.routes.decorators import role_required, SECRET_KEY

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
def list_users():
    conn = get_db()
    users = get_all_users(conn)
    return jsonify(users)


@users_bp.route('/get_by_id/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    conn = get_db()
    user = get_user_by_id_query(conn, str(user_id))
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user)

@users_bp.route('/get_by_nickname/<nickname>', methods=['GET'])
def get_user_by_nickname(nickname):
    conn = get_db()
    user = get_user_by_nickname_query(conn, str(nickname))
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user)

@users_bp.route('/role/<uuid:user_id>', methods=['PUT'])
@role_required(['admin'])
def update_user_role(user_id):
    data = request.json
    conn = get_db()
    update_user_role(
        conn,
        str(user_id),
        data['new_role_id']
    )
    return jsonify({"updated role for user": user_id}), 200

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    role_id = data['role_id']
    login = data.get('login')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone_number')
    age = data.get('age')

    if not all([name, login, password, age, phone_number]):
        return jsonify({"error": "Все поля обязательны"}), 400

    conn = get_db()
    try:
        user_id = create_user(conn,
                              role_id,
                              login,
                              password,
                              name,
                              phone_number,
                              age
                              )
        return jsonify({"message": "Пользователь зарегистрирован",
                        "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    nickname = data.get('login')
    password = data.get('password')

    if not all([nickname, password]):
        return jsonify({"error": "Все поля обязательны"}), 400

    conn = get_db()
    try:
        user = get_user_by_nickname_query(conn, nickname)

        if user is None:
            return jsonify({"error": "Неверный email или пароль"}), 401

        user_id, stored_password = user
        if password != stored_password:
            return jsonify({"error": "Неверный email или пароль"}), 401

        # Логирование значений
        print(f"user_id: {user_id}, SECRET_KEY: {SECRET_KEY}")

        token = jwt.encode(
            {
                "user_id": str(user_id),  # Убедитесь, что user_id строка
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            str(SECRET_KEY),  # Убедитесь, что SECRET_KEY строка
            algorithm="HS256"
        )

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

