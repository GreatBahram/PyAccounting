# third-party imports
from flask import flash, redirect, render_template, url_for
from flask_login import login_required

# local imports
from pyaccounting.user.forms import AddPurchaseForm
from . import user
from .. import db
from pyaccounting.models import PaymentModel

@user.route('/add_purchase', methods=["GET", "POST"])
@login_required
def add_purchase():
    """
    Handle requrests for the /addpurchase route
    add an new purchase to the database through add purchase form
    """
    form = AddPurchaseForm()
    if form.validate_on_submit():
        print('')

    return render_template('user/add_purchase.html', title="Add Purchase",
            form=form)
