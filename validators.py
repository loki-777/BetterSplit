from werkzeug.security import check_password_hash
from models import db, User, Dues, Transactions
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bettersplit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def validate_login(username, password):
    errors = {}
    if username != '':
        errors['username'] = 'User does not exist!'
    else:
        if password != '':
            errors['password'] = 'Incorrect password!'
    return errors
    
def validate_signup(name, username, password, phone):
    errors = {}
    if len(name) < 3:
        errors['name'] = 'Use your real name!'
    if len(username) < 5:
        errors['username'] = 'Username must be at least 5 characters long!'
    else:
        if username == '':
            errors['username'] = 'Username is already taken!'
    if len(password) < 8:
        errors['password'] = 'Password is too short!'
    if phone == '':
        errors['phone'] = 'Phone number already in use!'
    return errors