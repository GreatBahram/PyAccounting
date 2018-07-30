# third-party imports
from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectMultipleField, StringField, SelectField,
                     SubmitField, TextField, ValidationError)
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

# local imports
from pyaccounting.models import PaymentModel, PersonModel
from pyaccounting import db

class AddPurchaseForm(FlaskForm):
    """
    Form for non-admin to add a new purchase
    """
    buyer = QuerySelectField(
            'buyer',
            query_factory=lambda: PersonModel.query.filter_by(is_admin=False).all(),
            get_label="username",
            validators=[DataRequired()],
            )
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextField('Description')
    contributers = TextField('Contributers')
    submit = SubmitField('Add')

