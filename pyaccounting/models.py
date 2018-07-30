#!/usr/bin/env python3
# Author: GreatBahram

# third-party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# local imports
from pyaccounting import db, login_manager

class PersonModel(UserMixin, db.Model):
    """
        Create a Person table
    """

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    is_admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())

    @property
    def password(self):
        """
        Prevent password from being accessed.

        """
        raise AttributeError("Password is not readable attribute.")

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Checked if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                }

    def __repr__(self):
        return f"<Person: '{self.username}' '{self.email}'>"

# setup user_loader
@login_manager.user_loader
def load_user(user_id):
    return PersonModel.query.get(int(user_id))


class PaymentModel(db.Model):
    """
        Create a Payment table
    """

    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    buyer = db.Column(db.Integer, db.ForeignKey('persons.id'))
    debtor = db.Column(db.Integer, db.ForeignKey('persons.id'))
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    is_sale = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())

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
        return f"<Payment:>"

