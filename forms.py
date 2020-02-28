from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, ValidationError
from wtforms.validators import InputRequired, DataRequired

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