# Author: GreatBahram
"""Script for initializaing your database.

Note that dropping your existing tables is an opt-in operation.
If you want to drop tables before you create tables, set an environment-
variable called "DROPDB" to be "True".
"""
import os

from counting import db
from counting.models import Person

if bool(os.environ.get('DROPDB', '')):
    db.drop_all()

db.create_all()
