def register_routes(app):
    from .myuser import users_bp
    app.register_blueprint(users_bp, url_prefix='/user')

    from .action_log import action_logs_bp
    app.register_blueprint(action_logs_bp, url_prefix='/logs')

    from .role import roles_bp
    app.register_blueprint(roles_bp, url_prefix='/role')

    from .service import services_bp
    app.register_blueprint(services_bp, url_prefix='/service')

    from .promotions import promotions_bp
    app.register_blueprint(promotions_bp, url_prefix='/promotion')

    from .plane import planes_bp
    app.register_blueprint(planes_bp, url_prefix='/plane')

    from .flight import flights_bp
    app.register_blueprint(flights_bp, url_prefix='/flight')

    from .booking import bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/booking')

    from .review import reviews_bp
    app.register_blueprint(reviews_bp, url_prefix='/review')

    from .question import questions_bp
    app.register_blueprint(questions_bp, url_prefix='/question')

    from .myuser_service import myuser_service_bp
    app.register_blueprint(myuser_service_bp, url_prefix='/user-service')

