# setup_db.py
from app import create_app, db
from app.models import User, Role  # Import models here

app = create_app()

with app.app_context():
    db.create_all()
    # Optionally, we can add initial data to your database here
    # For example, creating default roles
    if not Role.query.first():
        admin_role = Role(name='admin', permissions='all')
        user_role = Role(name='user', permissions='read')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
    print("Database tables created successfully.")
