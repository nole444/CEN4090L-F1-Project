from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    
    # Import your routes
    from .routes import main  # Assuming you're using a blueprint named 'main'
    
    # Register the blueprint
    app.register_blueprint(main)
    
    return app
