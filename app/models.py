# app/models.py

from datetime import datetime
from app import db, login_manager, bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model with password hashing and authentication methods
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(130), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref='users')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Role model for role-based access control
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    permissions = db.Column(db.String(200), nullable=False)

# SimulationResult model to store user guesses and simulation outcomes
class SimulationResult(db.Model):
    __tablename__ = 'simulation_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=False)
    driver_number = db.Column(db.Integer, nullable=False)
    selected_time = db.Column(db.String(50), nullable=False)
    selected_driver = db.Column(db.String(50), nullable=False)
    strategy_accuracy = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('simulations', lazy=True))
    race = db.relationship('Race', backref=db.backref('simulations', lazy=True))

    def __repr__(self):
        return f"<SimulationResult User:{self.user.username} Race:{self.race.location} Driver:{self.selected_driver}>"

# Race model to store race details
class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    circuit_key = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    race_date = db.Column(db.Date, nullable=False)


    def __repr__(self):
        return f"<Race {self.location} on {self.race_date}>"