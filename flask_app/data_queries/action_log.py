def get_all_action_logs(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM actionlog")
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при получении логов: {e}")
        raise