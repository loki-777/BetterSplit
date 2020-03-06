from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bettersplit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	username = db.Column(db.String(50), unique = True)
	password = db.Column(db.String(100))
	phone = db.Column(db.String(100), unique = True)
	plus = db.Column(db.Float)
	minus = db.Column(db.Float)
	net = db.Column(db.Float)

class Transactions(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	paid_by = db.Column(db.String(50))
	paid_to = db.Column(db.String(50))
	amount = db.Column(db.Float)
	remark = db.Column(db.String(500))
	timestamp = db.Column(db.DateTime, default = datetime.now)