# third-party imports
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_

# local imports
from pyaccounting.user.forms import AddPurchaseForm, AddPaybackForm
from . import user
from pyaccounting import db
from pyaccounting.models.person import PersonModel
from pyaccounting.models.payment import PaymentModel

@user.route('/add_purchase', methods=["GET", "POST"])
@login_required
def add_purchase():
    """
    Handle requrests for the /add_purchase route
    add an new purchase to the database through add purchase form
    """
    form = AddPurchaseForm()
    form.contributers.choices = [(person.id,person.username) for person in PersonModel.query.filter_by(is_admin=False).all()]
    #form.contributers.
    if form.validate_on_submit():
        buyer = form.buyer.data.id
        debtors = form.contributers.data
        price = form.price.data
        description = form.description.data
        date = form.date.data
        split_price = price // len(debtors)
        for deb in debtors:
            payment =  PaymentModel(buyer=buyer, debtor=deb, price=split_price, description=description, date=date)
            db.session.add(payment)
        db.session.commit()
        flash('Your new expenditure has been added!', 'success')
        return redirect(url_for('home.aboutpage'))

    return render_template('user/add_purchase.html', title="Add Purchase",
            form=form)

@user.route('/add_payoff', methods=["GET", "POST"])
@login_required
def add_payoff():
    """
    Handle requrests for the /add_off route
    add an new purchase to the database through add purchase form
    """
    form = AddPaybackForm()
    if form.validate_on_submit():
        buyer = form.buyer.data.id
        debtor = form.debtor.data.id
        price = form.price.data
        description = form.description.data
        date = form.date.data
        payment =  PaymentModel(buyer=buyer, debtor=debtor, price=price, description=description, date=date,
                            is_payoff=True)
        try:
            payment.save_to_db()
            flash('The payoff has been added!', 'success')
        except:
            flash('An error occurred saving the payoff to the database', 'danger')
            return redirect(url_for('user.add_payoff'))
        return redirect(url_for('user.list_payoffs'))
    return render_template('user/add_payoff.html', title="Add Payoff", form=form)

@user.route('/shoplist')
@login_required
def list_purchases():
    items = PaymentModel.list_all_purchases(current_user.id)
    print(items)

@user.route('/payofflist')
@login_required
def list_payoffs():
    items = PaymentModel.list_all_payoffs(current_user.id)
    print(items)
    return render_template('user/list_payoffs.html', title="Payoffs", payoffs=items)
