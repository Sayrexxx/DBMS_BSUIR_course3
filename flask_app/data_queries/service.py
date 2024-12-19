def create_service(conn, myuser_id, name, price):
    """
    Создает новый сервис.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO service (
                    id,
                    myuser_id,
                    name,
                    price
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s
                ) RETURNING id;
                """,
                (myuser_id, name, price)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании сервиса: {e}")
        raise


def get_service_by_id(conn, service_id):
    """
    Получает сервис по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM service
                WHERE id = %s;
                """,
                (service_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении сервиса с ID {service_id}: {e}")
        raise


def get_all_services(conn):
    """
    Получает все сервисы.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM service;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех сервисов: {e}")
        raise


def update_service(conn, service_id, myuser_id, name, price):
    """
    Обновляет данные сервиса.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE service
                SET myuser_id = %s,
                    name = %s,
                    price = %s
                WHERE id = %s;
                """,
                (myuser_id, name, price, service_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении сервиса {service_id}: {e}")
        raise


def delete_service(conn, service_id):
    """
    Удаляет сервис по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM service
                WHERE id = %s;
                """,
                (service_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении сервиса {service_id}: {e}")
        raise
