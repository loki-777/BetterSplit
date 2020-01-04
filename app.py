from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView

app = Flask(__name__)

app.config['SECRET_KEY'] = '45w1n15G4Y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///mnt/ext/ilsbb/creds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	username = db.Column(db.String(50), unique = True)
	password = db.Column(db.String(100))

# Checks whether username exists in database, if yes checks the entered password
def authenticate(username, password):
	exists = User.query.filter_by(username = username).first()
	if exists:
		return check_password_hash(User.query.filter_by(username = username).first().password, password)
	else:
		return 'dne'

# Checks whether username already exists, if yes returns true
def taken(username):
	exists = User.query.filter_by(username = username).first()
	if exists:
		return True
	else:
		return False

# Checks for sufficient password length (8 characters long)
def pass_strength_validator(password):
	if len(password) < 8:
		return True
	else:
		return False

# Inserts new user into database
def new(name, username, password):
	hashed = generate_password_hash(password)
	new_user = User(name = name, username = username, password = hashed)
	db.session.add(new_user)
	db.session.commit()

# Home page automatically redirects to login if no user is logged in currently, or to profile is session is active 
@app.route('/')
def home():
	if 'user' not in session:
		return redirect('/login')
	else:
		return redirect('/profile')

# TODO: User landing page
@app.route('/profile')
def user_landing():
	if 'user' not in session:
		return redirect('/login')
	return render_template('profile.html', name=session['name'])

# Stylize login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = {}
	if 'user' in session:
		return redirect('/profile')
	if request.method == 'POST':
		if request.form['username'] == '':
			error['username_empty'] = 'Enter username!'
		if request.form['password'] == '':
			error['pass_empty'] ='Enter password!'
		check = authenticate(request.form['username'], request.form['password'])
		if check == 'dne':
			error['user_dne'] = 'User does not exist. Would you like to sign up?'
		else:
			if not check:
				error['auth_fail'] = 'Incorrect password! Try again.'
		if not error:
			session['user'] = request.form['username']
			session['name'] = User.query.filter_by(username = request.form['username']).first().name
			return redirect('/profile')
	return render_template('login.html', error = error)

# Checks for existing username, password confirmation bool and throws respective errors
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = {}
	if 'user' in session:
		return redirect('/profile')
	if request.method == 'POST':
		if request.form['name'] == '':
			error['name_empty'] = 'Name can not be left blank!'
		if request.form['username'] == '':
			error['username_empty'] = 'Username can not be left blank!'
		if request.form['password'] == '':
			error['pass_empty'] = 'Password can not be left blank!'
		if taken(request.form['username']):
			error['user_taken'] = 'Username is already taken!'
		if pass_strength_validator(request.form['password']):
			error['weak_pass'] = 'Password is too short!'
		if not error:
			new(request.form['name'], request.form['username'], request.form['password'])
			session['user'] = request.form['username']
			session['name'] = request.form['name']
			return redirect('/profile')
	return render_template('signup.html', error = error)

if __name__ == "__main__":
	app.run(debug=True)