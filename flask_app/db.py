import psycopg2
from flask import g, current_app
from psycopg2 import OperationalError, Error


def get_db():
    if 'db' not in g:
        try:
            dsn = current_app.config.get('DATABASE_URL')
            if not dsn:
                raise ValueError("DATABASE_URL не задан в конфигурации приложения.")

            g.db = psycopg2.connect(dsn)
        except ValueError as e:
            current_app.logger.error(f"Ошибка конфигурации базы данных: {e}")
            raise
        except OperationalError as e:
            current_app.logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
        except Error as e:
            current_app.logger.error(f"Ошибка базы данных: {e}")
            raise
    return g.db


def close_db(exc=None):
    db = g.pop('db', None)
    if db is not None:
        try:
            db.close()
        except Error as e:
            current_app.logger.warning(f"Ошибка при закрытии соединения с базой данных: {e}")


def init_db(app):
    app.teardown_appcontext(close_db)
