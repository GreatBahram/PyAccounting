#!/usr/bin/env python3
# Author: GreatBahram
from flask import Flask

# Initialize the app
app = Flask(__name__)

# Load the config file
app.config.from_object('config.DevelopmentConfig')

# Load the views
from counting import views
