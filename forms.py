from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, ValidationError, FloatField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('USERNAME', validators = [
        DataRequired()
    ])
    password = PasswordField('PASSWORD', validators = [
        DataRequired()
    ])
    login = SubmitField('LOG IN')

class SignupForm(FlaskForm):
    name = StringField('NAME *', validators = [
        DataRequired()
    ])
    username = StringField('USERNAME *', validators = [
        DataRequired()
    ])
    password = PasswordField('PASSWORD *', validators = [
        DataRequired()
    ])
    phone = StringField('PHONE NUMBER *', validators = [
        DataRequired()
    ])
    signup = SubmitField('SIGN UP')

class GroupForm(FlaskForm):
    name = StringField('NAME *', validators = [
        DataRequired()
    ])

class QuickPayForm(FlaskForm):
    amount = StringField('AMOUNT', validators = [
        DataRequired()
    ])
    to = StringField('TO', validators = [
        DataRequired()
    ])