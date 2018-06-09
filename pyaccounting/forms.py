#!/usr/bin/env python3
# Author: GreatBahram
from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectField, SelectMultipleField,
                     StringField, SubmitField, TextField)
from wtforms.validators import DataRequired

from counting.dbhelper import DBHelper


class AddItem(FlaskForm):
    db_api = DBHelper()
    persons = db_api.return_persons()

    fullname_list = []
    for person in persons:
        _id, fullname = person[0], " ".join(person[1:])
        fullname_list.append((_id, fullname))
    buyer = SelectField('Buyer', choices=fullname_list, \
            validators=[DataRequired()], coerce=int)
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextField('Description')
    others = SelectMultipleField('Contributers', choices=fullname_list, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


class PayoffDebt(FlaskForm):
    db_api = DBHelper()
    persons = db_api.return_persons()
    fullname_list = []
    for person in persons:
        _id, fullname = person[0], " ".join(person[1:])
        fullname_list.append((_id, fullname))

    debtor = SelectField('Debtor', choices=fullname_list, \
            validators=[DataRequired()], coerce=int)

    price = IntegerField('Price', validators=[DataRequired()])

    description = TextField('Description')

    creditor = SelectField('Creditor', choices=fullname_list, \
            validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')

