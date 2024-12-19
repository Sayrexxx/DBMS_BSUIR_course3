def create_user(conn, role_id, login,
                password, name, phone_number,
                age):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO "myuser" 
                (
                    id, 
                    role_id, 
                    login, 
                    password,
                    name, 
                    phone_number,
                    age
                )
                VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (role_id, login, password, name, phone_number, age)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        raise Exception(f"Ошибка при создании юзера: {e}")


def get_user_by_nickname_query(conn, email):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, password FROM "myuser" WHERE login = %s
                """,
                (email,)
            )
            return cursor.fetchone()
    except Exception as e:
        raise Exception(f"Ошибка при получении пользователя по email: {e}")


def get_user_by_id_query(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, role_id, login, password, name, phone_number, age FROM "myuser"
                WHERE id = %s
                """,
                (user_id,)
            )
            return cursor.fetchone()
    except Exception as e:
        raise Exception(f"Ошибка при получении пользователя по ID: {e}")


def get_user_role_name(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT r."name" AS role_name
                FROM "myuser" u
                JOIN "role" r ON u.role_id = r.id
                WHERE u.id = %s;
                """,
                user_id
            )
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return None
    except Exception as e:
        print(f"Ошибка получения роли: {e}")
        return None



def update_user_role(conn, user_id, new_role_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE myuser
                SET role_id = %s
                WHERE id = %s
                """,
                (new_role_id, user_id)
            )
            conn.commit()
        return True
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при обновления роли юзера {user_id}: {e}"
        )
        raise


def get_all_users(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM myuser"
            )
            return cursor.fetchall()
    except Exception as e:
        from flask import current_app
        current_app.logger.error(
            f"Ошибка при обновления всех юзеров: {e}"
        )
        raise