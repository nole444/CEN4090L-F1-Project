from flask import Blueprint, render_template, request
from .services.openf1_service import racefinder, getalldata


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
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        driver = request.form.get('driver')
        if user_input and user_input.strip():
            result = getalldata(str(driver).split(' ')[2], user_input)
    return render_template('home.html', result=result)
