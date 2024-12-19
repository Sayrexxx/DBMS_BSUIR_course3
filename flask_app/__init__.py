from flask import Flask

from flask_app.db import init_db
from flask_app.routes import register_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object('flask_app.config.Config')

    init_db(app)

    register_routes(app)

    return app