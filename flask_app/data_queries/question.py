def get_all_questions(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM questions")
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при получении вопросов: {e}")
        raise


def get_question_by_id(conn, question_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM questions WHERE id = %s",
                           (question_id,))
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при получении вопроса с ID "
            f"{question_id}: {e}")
        raise


def create_question(conn, myuser_id, question):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO questions (
                    id,
                    myuser_id,
                    question
                ) VALUES (
                    gen_random_uuid(), %s, %s) 
                    RETURNING id
                """,
                (
                    myuser_id, question
                )
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при добавлении вопроса: {e}"
        )
        raise


def remove_question(conn, question_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM questions WHERE id = %s",
                           (question_id,))
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при удалении вопроса: {e}"
        )
        raise


def update_question(conn, question_id, myuser_id, question):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE questions
                SET myuser_id = %s,
                    question = %s
                WHERE id = %s
                """,
                (
                    myuser_id,
                    question,
                    question_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при обновлении вопроса: {e}"
        )
        return False


def answer_asked_question(conn, question_id, answer):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE questions
                SET answer = %s
                WHERE id = %s
                RETURNING id
                """,
                (answer, question_id)
            )
            conn.commit()
            updated_question_id = cursor.fetchone()
            if updated_question_id:
                return updated_question_id[0]
            else:
                return None
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении ответа: {e}")
        raise