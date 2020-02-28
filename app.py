from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Dues, Transactions
from forms import LoginForm, SignupForm

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bettersplit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'c657a0b975d04adeb488661ceeb983cf'

db.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html', form = LoginForm())

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html', form = SignupForm())

if __name__ == '__main__':
    app.run(debug = True)