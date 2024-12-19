def create_booking(conn, flight_id, myuser_id, seats_amount, price):
    """
    Создает бронирование.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO booking (
                    id,
                    flight_id,
                    myuser_id,
                    seats_amount,
                    price,
                    datetime_created
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s, %s, DEFAULT
                ) RETURNING id;
                """,
                (flight_id, myuser_id, seats_amount, price)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при создании бронирования: {e}")
        raise


def get_booking_by_id(conn, booking_id):
    """
    Получает бронирование по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM booking
                WHERE id = %s;
                """,
                (booking_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении бронирования с ID {booking_id}: {e}")
        raise


def get_all_bookings(conn):
    """
    Получает все бронирования.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM booking;
                """
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении всех бронирований: {e}")
        raise


def update_booking(conn, booking_id, seats_amount, price):
    """
    Обновляет данные бронирования.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE booking
                SET seats_amount = %s,
                    price = %s
                WHERE id = %s;
                """,
                (seats_amount, price, booking_id)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при обновлении бронирования {booking_id}: {e}")
        raise


def delete_booking(conn, booking_id):
    """
    Удаляет бронирование по ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM booking
                WHERE id = %s;
                """,
                (booking_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении бронирования {booking_id}: {e}")
        raise
