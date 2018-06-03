#!/usr/bin/env python3
# Author: GreatBahram
from .app import db
from datetime import datetime

class Person(db.Model):
    """
        Create a Person table
    """

    __tablename__ == 'persons'

    id = db.Column(db.Integer, primary_key=True, autincrement=True)
    forename = db.Column(db.String(60), nullable=False) 
    surname = db.Column(db.String(60), nullable=False) 

    def to_dict(self):
        return {
                'id': self.id,
                'forname': self.forname,
                'surname': self.surname,
                }
    def __repr__(self):
        return "<Person: {} {}>".format(self.forename, self.surname)


class Payment(db.Model):
    """
        Create a Payment table
    """

    __tablename__ == 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Datetime, nullable=False)
    buyer = db.Column(db.Integer, db.ForeinKey('persons.id'))
    debtor = db.Column(db.Integer, db.ForeinKey('persons.id'))
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    is_sale = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
                'id': self.id,
                'date': self.date,
                'buyer': self.buyer,
                'debtor': self.debtor,
                'price': self.price,
                'description': self.description,
                'is_sale': self.is_sale,
                }

    def __repr__(self):
        return "<Payment:>"

