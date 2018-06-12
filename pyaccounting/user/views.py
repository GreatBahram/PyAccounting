# third-party imports
from flask import flash, redirect, render_template, url_for
from flask_login import login_required

# local imports
from .forms import AddPurchase
from . import user
from .. import db
from ..models import Payment

@user.route('/add_purchase', methods=["GET", "POST"])
def add_purchase():
    """
    Handle requrests for the /addpurchase route
    add an new purchase to the database through add purchase form
    """
    form = AddPurchase()
    print(form)
    if form.validate_on_submit():
        pass

    return render_template('user/add_purchase.html', title="Add Purchase",
            form=form)
