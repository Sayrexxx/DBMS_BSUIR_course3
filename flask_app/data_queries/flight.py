def create_flight(conn, service_id, origin_point, destination_point,
                  departure_datetime, arrival_datetime, price, plane_id=None):
    """
    Создает новый рейс.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO flight (
                    id,
                    service_id,
                    origin_point,
                    destination_point,
                    departure_datetime,
                    arrival_datetime,
                    price,
                    is_active,
                    plane_id
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s, %s, %s, %s, TRUE, %s
                ) RETURNING id;
                """,
                (service_id, origin_point, destination_point, departure_datetime,
                 arrival_datetime, price, plane_id)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании рейса: {e}")
        raise


def get_flight_by_id(conn, flight_id):
    """
    Получает рейс по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM flight
                WHERE id = %s;
                """,
                (flight_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении рейса с ID {flight_id}: {e}")
        raise


def get_all_flights(conn):
    """
    Получает все рейсы.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM flight;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех рейсов: {e}")
        raise


def update_flight(conn, flight_id, service_id, origin_point, destination_point,
                  departure_datetime, arrival_datetime, price, is_active=True, plane_id=None):
    """
    Обновляет данные рейса.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE flight
                SET service_id = %s,
                    origin_point = %s,
                    destination_point = %s,
                    departure_datetime = %s,
                    arrival_datetime = %s,
                    price = %s,
                    plane_id = %s
                WHERE id = %s;
                """,
                (service_id, origin_point, destination_point, departure_datetime,
                 arrival_datetime, price, plane_id, flight_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении рейса {flight_id}: {e}")
        raise


def delete_flight(conn, flight_id):
    """
    Удаляет рейс по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM flight
                WHERE id = %s;
                """,
                (flight_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении рейса {flight_id}: {e}")
        raise
