#!/usr/bin/env python3
# Author: GreatBahram

# third-part imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
bcrypt = Bcrypt()

# login_manager variable initialization
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    Bootstrap(app)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)
    from pyaccounting import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
