from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import InputRequired, DataRequired

class LoginForm(FlaskForm):
    username = StringField('USERNAME')
    password = PasswordField('PASSWORD')
    login = SubmitField('LOG IN')

class SignupForm(FlaskForm):
    name = StringField('NAME')
    username = StringField('USERNAME')
    password = PasswordField('PASSWORD')
    phone = StringField('PHONE NUMBER')
    signup = SubmitField('SIGN UP')