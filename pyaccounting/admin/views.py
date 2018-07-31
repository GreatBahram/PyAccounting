# third-party imports
from flask_login import current_user, login_required
from flask import abort, flash, redirect, render_template, request, url_for

# local imports
from . import admin
from pyaccounting import db
from pyaccounting.admin.forms import PersonForm
from pyaccounting.models import PersonModel

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/persons')
@login_required
def list_persons():
    """
    List all employees
    """
    check_admin()
    page = request.args.get('page', 1, type=int)
    persons = PersonModel.query.filter_by(is_admin=False).paginate(per_page=10, page=page)
    return render_template('admin/persons/persons.html', persons=persons, title="Persons")

@admin.route('/persons/add', methods=['GET', 'POST'])
@login_required
def add_person():
    """
    Add a person to the database
    """
    check_admin()

    add_user = True

    form = PersonForm()
    if form.validate_on_submit():
        person = PersonModel(
                username=form.username.data,
                email=form.email.data,
                password_hash=form.password.data,
                )
        # save to the database
        db.session.add(person)
        db.session.commit()

        # redirect to persons page
        return redirect(url_for('admin.list_persons'))

    # load persons template
    return render_template('admin/persons/person.html', form=form, title="Add Person", add_user=add_user)

@admin.route('/persons/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_person(id):
    """
    Edit a person
    """
    check_admin()

    add_user = False
    
    person = PersonModel.query.get_or_404(id)
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        if form.password.data:
            person.password = form.password.data
        person.email = form.email.data
        person.username = form.username.data

        db.session.commit()
        flash('You have successfully edited the person', 'success')

        # redirect to persons page
        return redirect(url_for('admin.list_persons'))

    form.email.data = person.email
    form.username.data = person.username
    form.password.data = ""

    # load persons template
    return render_template('admin/persons/person.html', form=form, title="Edit Person", add_user=add_user, person=person)

@admin.route('/persons/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_person(id):
    """
    Delete a person
    """
    check_admin()

    add_user = False

    person = PersonModel.query.get_or_404(id)

    db.session.delete(person)
    db.session.commit()
    flash('You have successfully deleted the person.', 'success')

    # redirect to the departments page
    return redirect(url_for('admin.list_persons'))
