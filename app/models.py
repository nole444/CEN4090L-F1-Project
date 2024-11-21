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
    __tablename__ = 'users'  # Optional: specify table name

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
    __tablename__ = 'roles'  # Optional: specify table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    permissions = db.Column(db.String(200), nullable=False)
