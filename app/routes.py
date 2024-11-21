# routes.py
#This file will contain the html routes using flask

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import RegistrationForm, LoginForm
from . import db, bcrypt
import re



main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('home.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            role_id=1  # Assuming a default role ID
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main_bp.login'))
    return render_template('register.html', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        input_data = form.email_or_username.data
        # Simple regex to check if input is an email
        if re.match(r"[^@]+@[^@]+\.[^@]+", input_data):
            user = User.query.filter_by(email=input_data).first()
        else:
            user = User.query.filter_by(username=input_data).first()

        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main_bp.account'))
        else:
            flash('Login Unsuccessful. Please check your credentials.', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_bp.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Integrate with the F1 API to display race data
    return render_template('dashboard.html')

@main_bp.route('/account')
@login_required
def account():
    # Since badges and races aren't implemented yet we will pass empty lists for now
    races = []  # Placeholder
    racers = []  # Assuming you have a Racer model
    badges = []  # Placeholder

    return render_template('account.html', races=races, racers=racers, badges=badges)
@main_bp.route('/user_stats')
@login_required
def user_stats():
    # Fetch user-specific statistics
    stats = {}  # Placeholder for user stats data
    return render_template('user_stats.html', stats=stats)

