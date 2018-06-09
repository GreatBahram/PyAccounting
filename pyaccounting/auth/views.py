# third-party imports
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

# local imports
from .forms import LoginForm, RegisterationForm
from . import auth
from .. import db
from ..models import Person


@auth.route('/register', methods=["GET", "POST"])
def register():
    """
        Handle requests to the /register route
        Add an employee to the database through the registration form
    """
    form = RegisterationForm()
    if form.validate_on_submit():
        person = Person(
            username=form.username.data,
            email=form.email.data,
            forename=form.forename.data,
            surname=form.surname.data,
            password=form.password.data,
                )
        # add person to the database
        db.session.add(person)
        db.session.commit()
        flash("You have successfully registered! You may now login.")

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registeration template
    return render_template('auth/register.html', form=form, title="Register")

@auth.route('/login', methods=["GET", "POST"])
def login():
    """
        Handle requests to the /login route
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check where person exists in our database or not
        person = Person.query.filter_by(email=form.email.data).first()

        if person is not None and person.verify_password(
                form.password.data):
            # log person in
            login_user(person)
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title="Login")

@auth.route('/logout')
@login_required
def logout():
    """
        Handle requests to the /logout route
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
