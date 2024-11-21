# config.py

import os

class Config:
    SECRET_KEY = '5623'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:noles2021@localhost/F1_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False