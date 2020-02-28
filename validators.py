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
    existing_user = User.query.filter_by(username = username).first()
    if not existing_user:
        errors['username'] = 'User does not exist!'
    else:
        if not check_password_hash(existing_user.password, password):
            errors['password'] = 'Incorrect password!'
    return errors

def validate_signup(name, username, password, phone):
    errors = {}
    if len(name) < 3:
        errors['name'] = 'Use your real name!'
    if len(username) < 5:
        errors['username'] = 'Username must be at least 5 characters long!'
    else:
        username_taken = User.query.filter_by(username = username).first()
        if username_taken:
            errors['username'] = 'Username is already taken!'
    if len(password) < 8:
        errors['password'] = 'Password is too short!'
    if len(phone) != 10:
        errors['phone'] = 'Invalid phone number!'
    else:
        phone_taken = User.query.filter_by(phone = phone).first()
        if phone_taken:
            errors['phone'] = 'Phone number already in use!'
    return errors