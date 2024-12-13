# routes.py
#This file will contain the html routes using flask

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import RegistrationForm, LoginForm
from . import db, bcrypt
import re
from .forms import RaceForm, GuessForm
from .services.openf1_service import racefinder
from .services.openf1_service import driver_dict
from .services.sim import simEngine
import random




main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Initialize forms
    race_form = RaceForm()
    guess_form = GuessForm()

    # Define available strategies
    strategies = [
        'Aggressive', 'Defensive', 'Balanced',
        'Medium Aggressive', 'Medium Balanced', 'Conservative'
    ]
    # Populate strategy choices
    guess_form.strategy.choices = [(s.lower(), s) for s in strategies]

    # Retrieve any previously found races from session
    races_found = session.get('races_found', [])
    simulation_results = {}
    strategy_accuracy = None
    driver_selected = None
    timing_board = []
    real_race_results = []
    participating_drivers = []

    # Determine driver choices before handling POST, so validation can pass
    if races_found:
        selected_race = races_found[0]
        participating_drivers = selected_race.get('participating_drivers', [])
        # If no simulation is done yet, populate drivers from participating drivers
        if participating_drivers:
            guess_form.driver.choices = [(num, driver_dict.get(num, "Unknown Driver")) for num in participating_drivers]
        else:
            # If no participating drivers, fallback to all known drivers
            guess_form.driver.choices = [(num, name) for num, name in driver_dict.items()]
    else:
        # If no races found, default to all drivers
        guess_form.driver.choices = [(num, name) for num, name in driver_dict.items()]

    if request.method == 'POST':
        submit_type = request.form.get('submit', '')

        if submit_type == 'Find Races' and race_form.validate_on_submit():
            # Handle RaceForm submission
            date_input = race_form.race_date.data.strftime('%Y-%m-%d')
            races_found = racefinder(date_input)
            session['races_found'] = races_found  # Store in session

            if races_found:
                flash('Races found on the selected date.', 'success')
                selected_race = races_found[0]
                circuit_name = selected_race['circuit_details']['circuit_name']
                participating_drivers = selected_race.get('participating_drivers', [])
                real_race_results = selected_race.get('real_results', [])
                flash(f"Selected Race: {circuit_name}", 'info')

                # Update driver choices now that we have a selected race
                if participating_drivers:
                    guess_form.driver.choices = [(num, driver_dict.get(num, "Unknown Driver")) for num in participating_drivers]
                else:
                    guess_form.driver.choices = [(num, name) for num, name in driver_dict.items()]

            else:
                flash('No races found on the selected date or no participating drivers available.', 'warning')
                session.pop('races_found', None)
                guess_form.driver.choices = [(num, name) for num, name in driver_dict.items()]

        elif submit_type == 'Submit Guess' and guess_form.validate_on_submit():
            # Handle GuessForm submission
            races_found = session.get('races_found', [])
            if not races_found:
                flash('No race selected for simulation.', 'danger')
                return redirect(url_for('main_bp.account'))

            selected_strategy_name = guess_form.strategy.data.capitalize()
            selected_driver_number = int(guess_form.driver.data)
            selected_driver = driver_dict.get(selected_driver_number, "Unknown Driver")

            # Get participating drivers from race data
            selected_race = races_found[0]
            participating_drivers = selected_race.get('participating_drivers', [])
            real_race_results = selected_race.get('real_results', [])
            if not participating_drivers:
                flash('No participating drivers found for the selected race.', 'danger')
                return redirect(url_for('main_bp.account'))

            if selected_driver_number not in participating_drivers:
                flash('Selected driver is not participating in the selected race.', 'danger')
                return redirect(url_for('main_bp.account'))

            APIdata = {
                'driver_number': selected_driver_number,
                'circuit_key': selected_race['circuit_details']['circuit_key']
            }

            grid = participating_drivers.copy()
            simulation_results = simEngine(APIdata, selected_strategy_name, grid, real_race_results)

            timing_board = simulation_results.get('timing_board', [])
            strategy_accuracy = simulation_results.get('strategy_accuracy', 0)
            driver_selected = selected_driver
            real_race_results = simulation_results.get('real_results', [])

            flash(f'Simulation completed. Closeness: {strategy_accuracy:.2f}%', 'info')

            # Optionally clear races_found from session after simulation
            session.pop('races_found', None)

    return render_template('account.html',
                           races_found=races_found,
                           driver_dict=driver_dict,
                           race_form=race_form,
                           guess_form=guess_form,
                           result=strategy_accuracy,
                           driver_selected=driver_selected,
                           timing_board=timing_board,
                           real_race_results=real_race_results,
                           participating_drivers=participating_drivers)

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


@main_bp.route('/user_stats')
@login_required
def user_stats():
    # Fetch user-specific statistics
    stats = {}  # Placeholder for user stats data
    return render_template('user_stats.html', stats=stats)

