from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from backend.routes import todo_routes
    app.register_blueprint(todo_routes.todo_routes)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)
