from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '45w1n15G4Y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ilsbb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO: Modularize this program into several components

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	username = db.Column(db.String(50), unique = True)
	password = db.Column(db.String(100))

class Dues(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50))
	plus = db.Column(db.Float)
	minus = db.Column(db.Float)
	net = db.Column(db.Float)

class Transactions(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	paid_by = db.Column(db.String(50))
	paid_to = db.Column(db.String(50))
	amount = db.Column(db.Float)
	remark = db.Column(db.String(500))
	timestamp = db.Column(db.DateTime, default=datetime.now)

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
def add_user(name, username, password):
	hashed = generate_password_hash(password)
	new_user = User(name = name, username = username, password = hashed)
	init_debt = Dues(username = username, plus = 0, minus = 0)
	db.session.add(new_user)
	db.session.add(init_debt)
	db.session.commit()

# Inserts new transaction into database
def add_transaction(paid_to, amount, remark):
	new_transaction = Transactions(paid_by = session['user'], paid_to = paid_to, amount = amount, remark = remark)	
	db.session.add(new_transaction)
	db.session.commit()

# Updates account
def update_account(paid_to, amount):
	sender = Dues.query.filter_by(username = session['user']).first()
	recipient = Dues.query.filter_by(username = paid_to).first()
	sender.minus += float(amount)
	sender.net = sender.plus - sender.minus
	recipient.plus += float(amount)
	recipient.net = recipient.plus - recipient.minus
	db.session.commit()

# Home page automatically redirects to login if no user is logged in currently, or to profile is session is active 
@app.route('/')
def home():
	if 'user' not in session:
		return redirect('/login')
	else:
		return redirect('/profile')

# TODO: Styles for user landing page
@app.route('/profile', methods=['GET', 'POST'])
def user_landing():
	error = {}
	recent_tranlist = []
	userslist = []
	if 'paid' not in session:
		session['paid'] = False
	if 'user' not in session:
		return redirect('/login')
	if session['paid']:
		return redirect('/paid')
	elif request.method == 'POST':
		if request.form['amount'] == '' or float(request.form['amount']) == 0:
			error['empty_amount'] = 'Enter amount!'
		if request.form['pay_to'] == 'none':
			error['empty_payee'] = 'Choose payee!'
		# TODO: Fix remark error if made mandatory 
		if request.form['remark'] == '':
			error['empty_remark'] = 'Enter remark!'
		if not error:
			amount_abs = abs(float(request.form['amount']))
			add_transaction(request.form['pay_to'], amount_abs, request.form['remark'])
			update_account(request.form['pay_to'], amount_abs)
			session['paid'] = True
	
	# TODO: Devise a more efficient algorithm to sort this list in descending order of id
	by_list = list(Transactions.query.filter_by(paid_by = session['user']))
	to_list = list(Transactions.query.filter_by(paid_to = session['user']))
	by_list.reverse()
	to_list.reverse()
	recent_tranlist = by_list + to_list
	def return_id(val):
		return val.id
	recent_tranlist.sort(key = return_id, reverse=True)
	i = int(0)
	recent_transactions = []
	for tran in recent_tranlist:
		if i < 10:
			recent_transactions.append(tran)
			i += 1
		else:
			break
	for tran in recent_transactions:
		tran.paid_by = User.query.filter_by(username = tran.paid_by).first().name
		tran.paid_to = User.query.filter_by(username = tran.paid_to).first().name
	userslist = User.query
	return render_template('profile.html', name=session['name'], recent_transactions=recent_transactions, userbase=userslist, error=error)

# Intermediate redirect to reset session variable
@app.route('/paid', methods=['GET'])
def paid():
	session['paid'] = False
	return redirect('/profile')

# Settle data
@app.route('/settle')
def settle():
	amount = float(0)
	username = ''
	due_table = list(Dues.query)
	due_nonzero_list = []
	for item in due_table:
		if item.net != 0:
			due_nonzero_list.append(item)
	due_nonzero_list.sort(key = lambda x: x.net)
	i = int(0)
	prev_name = ''
	prev_amt = float(0)
	dict_pay_pair = {}
	for item in due_nonzero_list:
		if i != 0:
			dict_pay_pair[prev_name] = (item.username, prev_amt)
		prev_name = item.username
		prev_amt += float(item.net)
		i += 1
	if session['user'] in dict_pay_pair.keys():
		username = dict_pay_pair[session['user']][0]
		amount = abs(dict_pay_pair[session['user']][1])
	return render_template('settle.html', amount = amount, username = username)

# Login page
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
			add_user(request.form['name'], request.form['username'], request.form['password'])
			session['user'] = request.form['username']
			session['name'] = request.form['name']
			return redirect('/profile')
	return render_template('signup.html', error = error)

if __name__ == "__main__":
	app.run(debug=True)
