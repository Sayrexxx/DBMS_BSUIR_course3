def create_plane(conn, available_seats, model, company):
    """
    Создает самолет.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO plane (
                    id,
                    available_seats,
                    model,
                    company
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s
                ) RETURNING id;
                """,
                (available_seats, model, company)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании самолета: {e}")
        raise


def get_plane_by_id(conn, plane_id):
    """
    Получает самолет по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM plane
                WHERE id = %s;
                """,
                (plane_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении самолета с ID {plane_id}: {e}")
        raise


def get_all_planes(conn):
    """
    Получает все самолеты.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM plane;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех самолетов: {e}")
        raise


def update_plane(conn, plane_id, available_seats, model, company):
    """
    Обновляет данные самолета.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE plane
                SET available_seats = %s,
                    model = %s,
                    company = %s
                WHERE id = %s;
                """,
                (available_seats, model, company, plane_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении самолета {plane_id}: {e}")
        raise


def delete_plane(conn, plane_id):
    """
    Удаляет самолет по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM plane
                WHERE id = %s;
                """,
                (plane_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении самолета {plane_id}: {e}")
        raise
