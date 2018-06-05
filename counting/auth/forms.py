# third-part imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

# local imports
from ..models import Person

class RegisterationForm(FlaskForm):
    """
    Form for admin to create a new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), 
            EqualTo('confirm_password')]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(field):
        if Person.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(field):
        if Person.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Login')

