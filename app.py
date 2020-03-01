from flask import Flask, render_template, redirect, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from validators import validate_login, validate_signup, validate_quickpay
from forms import LoginForm, SignupForm, QuickPayForm
from models import db, User, Dues, Transactions
from flask_sqlalchemy import SQLAlchemy
from transactors import quick_pay
from parsers import parse_dues

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bettersplit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'c657a0b975d04adeb488661ceeb983cf'

db.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect('/login')
    username = session['user']
    form = QuickPayForm(request.form)
    errors = {}
    if request.method == 'POST':
        errors = validate_quickpay(
            form.amount.data,
            form.to.data
        )
        if not errors:
            quick_pay(
                form.amount.data,
                form.to.data,
                username
            )
    profile_query = User.query.filter_by(username = username).first()
    profile = {
        'username' : profile_query.username,
        'name' : profile_query.name,
        'phone' : profile_query.phone
    }
    due_query = Dues.query.filter_by(username = username).first()
    dues = parse_dues(due_query)
    dues = {
        'plus' : dues['plus'],
        'minus' : dues['minus'],
        'net' : dues['net']
    }
    return render_template(
        'home.html',
        form = form,
        errors = errors,
        profile = profile,
        dues = dues
    )

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')
    form = LoginForm(request.form)
    errors = {}
    if request.method == 'POST':
        errors = validate_login(
            form.username.data,
            form.password.data
        )
        if not errors:
            session['user'] = request.form['username']
            return redirect('/')
    return render_template(
        'login.html',
        form = form,
        errors = errors
    )

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect('/')
    form = SignupForm()
    errors = {}
    if request.method == 'POST':
        errors = validate_signup(
            form.name.data,
            form.username.data,
            form.password.data,
            form.phone.data
        )
        if not errors:
            gpay_bool = 'gpay' in request.form
            paytm_bool = 'paytm' in request.form
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                name = form.name.data,
                username = form.username.data,
                password = hashed_password,
                phone = form.phone.data,
                gpay = gpay_bool,
                paytm = paytm_bool
            )
            new_due = Dues(
                username = form.username.data,
                plus = 0,
                minus = 0,
                net = 0
            )
            db.session.add(new_user)
            db.session.add(new_due)
            db.session.commit()
            session['user'] = request.form['username']
            return redirect('/')
    return render_template(
        'signup.html',
        form = form,
        errors = errors
    )

@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug = True)