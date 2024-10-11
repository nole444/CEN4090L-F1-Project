from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = '5623'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:noles2021@localhost/F1_DB'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Database setup complete.")