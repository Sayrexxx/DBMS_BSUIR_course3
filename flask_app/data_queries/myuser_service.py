def add_service_to_user_query(conn, myuser_id, service_id):
    """
    Добавляет услугу пользователю (создает запись в MyUser_service).
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO myuser_service (
                    id,
                    MyUser_id,
                    service_id
                ) VALUES (
                    gen_random_uuid(), %s, %s
                ) RETURNING id;
                """,
                (myuser_id, service_id)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при добавлении услуги пользователю: {e}")
        raise


def remove_service_from_user_query(conn, myuser_service_id):
    """
    Удаляет услугу у пользователя (удаляет запись в MyUser_service).
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM myuser_service
                WHERE myuser_service.id = %s;
                """,
                (myuser_service_id,)
            )
            conn.commit()
            return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при удалении услуги у пользователя: {e}")
        raise


def get_services_by_user(conn, myuser_id):
    """
    Получает все услуги, связанные с пользователем по его ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.id, s.name, s.price
                FROM service s
                JOIN myuser_service mus ON s.id = mus.service_id
                WHERE mus.MyUser_id = %s;
                """,
                (myuser_id,)
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении услуг для пользователя {myuser_id}: {e}")
        raise


def get_users_by_service(conn, service_id):
    """
    Получает всех пользователей, связанные с услугой по ее ID.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.name, u.phone_number, u.age
                FROM myuser u
                JOIN myuser_service mus ON u.id = mus.MyUser_id
                WHERE mus.service_id = %s;
                """,
                (service_id,)
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Ошибка при получении пользователей для услуги {service_id}: {e}")
        raise
