from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class='backend.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.income import income_bp
    from backend.routes.expense import expense_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(income_bp, url_prefix="/transaction/income")
    app.register_blueprint(expense_bp, url_prefix="/transaction/expense")

    return app
