def create_promotion(conn, title, description, discount, end_date, service_id):
    """
    Создает новую акцию.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO promotions (
                    id,
                    title,
                    description,
                    discount,
                    end_date,
                    service_id
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s, %s, %s
                ) RETURNING id;
                """,
                (title, description, discount, end_date, service_id)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании акции: {e}")
        raise


def get_promotion_by_id(conn, promotion_id):
    """
    Получает акцию по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM promotions
                WHERE id = %s;
                """,
                (promotion_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении акции с ID {promotion_id}: {e}")
        raise


def get_all_promotions(conn):
    """
    Получает все акции.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM promotions;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех акций: {e}")
        raise


def update_promotion(conn, promotion_id, title, description, discount, end_date, service_id):
    """
    Обновляет информацию об акции.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE promotions
                SET title = %s,
                    description = %s,
                    discount = %s,
                    end_date = %s,
                    service_id = %s
                WHERE id = %s;
                """,
                (title, description, discount, end_date, service_id, promotion_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении акции {promotion_id}: {e}")
        raise


def delete_promotion(conn, promotion_id):
    """
    Удаляет акцию по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM promotions
                WHERE id = %s;
                """,
                (promotion_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении акции {promotion_id}: {e}")
        raise
