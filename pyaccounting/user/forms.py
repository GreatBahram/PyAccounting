# third-party imports
from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectMultipleField, StringField,
                     SubmitField, TextAreaField, TextField, ValidationError,
                     widgets)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

# local imports
from pyaccounting import db
from pyaccounting.models import PaymentModel, PersonModel


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
    description = TextAreaField('Description')
    contributers = MultiCheckboxField('Contributers', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')
