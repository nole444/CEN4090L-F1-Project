# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os



# Instantiate extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5623'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:noles2021@localhost/F1'

    # Initialize extensions that we are utilizing
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Configure login manager
    login_manager.login_view = 'login'

    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
