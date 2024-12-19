from flask_app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Rule: {rule}, Endpoint: {rule.endpoint}, Methods: {rule.methods}")
    app.run(debug=True)
