def create_review(conn, text, grade, myuser_id):
    """
    Создает новый отзыв.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reviews (
                    id,
                    text,
                    grade,
                    myuser_id
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s
                ) RETURNING id;
                """,
                (text, grade, myuser_id)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании отзыва: {e}")
        raise


def get_review_by_id(conn, review_id):
    """
    Получает отзыв по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM reviews
                WHERE id = %s;
                """,
                (review_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении отзыва с ID {review_id}: {e}")
        raise


def get_reviews_by_user_id(conn, myuser_id):
    """
    Получает все отзывы для пользователя по его ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM reviews
                WHERE myuser_id = %s;
                """,
                (myuser_id,)
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении отзывов для пользователя с ID {myuser_id}: {e}")
        raise


def get_all_reviews(conn):
    """
    Получает все отзывы.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM reviews;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех отзывов: {e}")
        raise


def update_review(conn, review_id, text, grade):
    """
    Обновляет текст и оценку отзыва.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE reviews
                SET text = %s,
                    grade = %s
                WHERE id = %s;
                """,
                (text, grade, review_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении отзыва {review_id}: {e}")
        raise


def delete_review(conn, review_id):
    """
    Удаляет отзыв по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM reviews
                WHERE id = %s;
                """,
                (review_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении отзыва {review_id}: {e}")
        raise
