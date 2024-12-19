import jwt
from functools import wraps
from flask import request, jsonify
from flask_app.db import get_db

SECRET_KEY = 'your_secret_key'  # Замените на ваш ключ

def role_required(allowed_roles):
    """
    Декоратор для проверки роли пользователя.

    :param allowed_roles: Список разрешённых ролей (например, ['admin', 'moderator']).
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Получаем токен из заголовка Authorization
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Отсутствует токен или неверный формат"}), 401

            token = auth_header.split(" ")[1]

            try:
                # Декодируем токен и получаем user_id
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_token.get("user_id")
                if not user_id:
                    return jsonify({"error": "Токен не содержит user_id"}), 401

                # Подключаемся к базе данных
                conn = get_db()
                with conn.cursor() as cursor:
                    # Достаем все данные пользователя из таблицы myuser
                    cursor.execute("""
                        SELECT * 
                        FROM myuser 
                        WHERE id = %s
                    """, (user_id,))
                    user_data = cursor.fetchone()

                    if not user_data:
                        return jsonify({"error": "Пользователь не найден"}), 404

                    # Извлекаем role_id из данных пользователя
                    role_id = user_data[1]
                    if not role_id:
                        return jsonify({"error": f"Роль пользователя не определена  {role_id}"}), 404

                    # Достаем имя роли по role_id
                    cursor.execute("""
                        SELECT name 
                        FROM role 
                        WHERE id = %s
                    """, (role_id,))
                    role_data = cursor.fetchone()

                    if not role_data:
                        return jsonify({"error": "Роль не найдена"}), 404

                    role_name = role_data[0]

                    # Проверяем, входит ли роль в список разрешённых
                    if role_name not in allowed_roles:
                        return jsonify({"error": "Недостаточно прав"}), 403

                # Если проверка прошла, вызываем декорируемую функцию
                return f(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Срок действия токена истек"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Неверный токен"}), 401
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        return decorated_function

    return decorator
