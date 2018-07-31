# third-party imports
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# local imports
from pyaccounting.models import PersonModel

class PersonForm(FlaskForm):
    """
    Form for admin to create a new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), 
            EqualTo('confirm_password')]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_email(self, field):
        if PersonModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
        if PersonModel.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')

