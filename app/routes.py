from flask import Blueprint, render_template, request
from .services.openf1_service import poll_positions, racefinder, getalldata
from datetime import datetime


# Define a blueprint (optional, but recommended for modularity)
main = Blueprint('main', __name__)

# Define a route for the home page


@main.route('/')
def home():
    return render_template('home.html')  # Renders the `home.html` template

# A route that runs Python code when the button is clicked

# 2024-09-22T13:03:47.458000+00:00


@main.route('/run-code', methods=['POST'])
def run_code():
    result = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input and user_input.strip():
            result = racefinder(user_input)
    return render_template('home.html', races_found=result)


@main.route('/get-data', methods=['POST'])
def get_data():
    result = None
    positions = None
    driver_selected = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        timestamp = int(user_input)
        dt_object = datetime.fromtimestamp(timestamp)
        user_input = dt_object.strftime("%Y-%m-%dT%H:%M:%S")
        driver = request.form.get('driver')
        driver_selected = str(driver).split(
            ' ')[0] + ' ' + str(driver).split(' ')[1]

        if user_input and user_input.strip():
            result = getalldata(str(driver).split(' ')[2], user_input)
            positions = poll_positions(
                result['datetime'], result['date_start'])
    return render_template('home.html', result=result, positions=positions, driver_selected=driver_selected)
