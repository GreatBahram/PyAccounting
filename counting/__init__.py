#!/usr/bin/env python3
# Author: GreatBahram

# third-part imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# login_manager variable initialization
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.message = "You must be logged in to access this page"

    migrate = Migrate(app, db)
    from counting import models

    return app
