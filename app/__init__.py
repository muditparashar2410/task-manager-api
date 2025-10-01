from flask import Flask
from .extensions import db, migrate, jwt
from .auth import auth_bp
from .resources import task_bp
from config import Config
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp)

    # Swagger template
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Task Manager API",
            "description": "API for managing tasks with JWT authentication",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "definitions": {
            "Task": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "completed": {"type": "boolean"},
                    "created_at": {"type": "string"},
                    "updated_at": {"type": "string"},
                    "user_id": {"type": "integer"}
                }
            }
        }
    }

    Swagger(app, template=swagger_template)
    return app
