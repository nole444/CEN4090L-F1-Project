# CEN4090L-F1-Project
# Running App in Terminal Commands

1. **Activate the Virtual Environment**:

    ```sh
    source venv/bin/activate
    ```

2. **Install Required Packages**:

    Make sure you have the following Flask packages installed. You can check by using the command `pip list`. If they are not installed, use the following command to install them:

    ```sh
    pip install Flask psycopg2-binary flask_sqlalchemy flask_bcrypt flask_login flask_migrate flask_wtf
    ```

3. **Start PostgreSQL Server**:

    ```sh
    sudo systemctl start postgresql
    ```

4. **Check PostgreSQL Status**:

    Make sure PostgreSQL is running:

    ```sh
    sudo systemctl status postgresql
    ```

5. **Set Up the Database**:

    Run the setup script to create initial database tables:

    ```sh
    python setup.py
    ```

6. **Set Flask App Environment Variable**:

    ```sh
    export FLASK_APP=app.py
    ```

7. **Initialize Flask-Migrate**:

    Initialize the migration repository (only needed the first time):

    ```sh
    flask db init
    ```

8. **Generate an Initial Migration**:

    ```sh
    flask db migrate -m "Initial migration Successful."
    ```

9. **Apply the Migration**:

    ```sh
    flask db upgrade
    ```

10. **Run the Flask Application**:

    ```sh
    flask run
    ```

