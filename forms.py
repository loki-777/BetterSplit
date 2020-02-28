from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators

class LoginForm(FlaskForm):
    username = StringField('USERNAME')
    password = PasswordField('PASSWORD')
    login = SubmitField('LOG IN')
    signupredirect = SubmitField('SIGN UP')

class SignupForm(FlaskForm):
    name = StringField('NAME')
    username = StringField('USERNAME')
    password = PasswordField('PASSWORD')
    phone = StringField('PHONE NUMBER')
    signup = SubmitField('SIGN UP')
    loginredirect = SubmitField('BACK TO LOGIN')