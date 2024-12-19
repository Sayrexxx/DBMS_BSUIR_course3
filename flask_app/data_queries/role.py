def create_role(conn, name):
    """
    Создает новую роль.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO role (
                    id,
                    name
                ) VALUES (
                    gen_random_uuid(), %s
                ) RETURNING id;
                """,
                (name,)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании роли: {e}")
        raise


def get_role_by_id(conn, role_id):
    """
    Получает роль по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM role
                WHERE id = %s;
                """,
                (role_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении роли с ID {role_id}: {e}")
        raise


def get_all_roles(conn):
    """
    Получает все роли.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM role;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех ролей: {e}")
        raise


def update_role(conn, role_id, name):
    """
    Обновляет данные роли.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE role
                SET name = %s
                WHERE id = %s;
                """,
                (name, role_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении роли {role_id}: {e}")
        raise


def delete_role(conn, role_id):
    """
    Удаляет роль по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM role
                WHERE id = %s;
                """,
                (role_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении роли {role_id}: {e}")
        raise
