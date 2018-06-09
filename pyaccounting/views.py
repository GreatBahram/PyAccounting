from flask import render_template

from counting import app
from counting.dbhelper import DBHelper
from counting.forms import AddItem, PayoffDebt

def replacement(tuple_row, names_dict):
    list_row = list(tuple_row)
    list_row[2] = names_dict.get(list_row[2], "NA")
    list_row[3] = names_dict.get(list_row[3], "NA")
    return list_row

@app.route('/')
@app.route('/index')
def index():
    # Calculate the money
    db_api = DBHelper()
    results = db_api.sum_for_all()
    return render_template('index.html', results=results)

@app.route('/add', methods=["POST", "GET"])
def add():
    form = AddItem()
    if form.validate_on_submit():
        db_api = DBHelper()
        db_api.add_new_item(form.buyer.data,
                form.others.data,
                form.price.data,
                form.description.data)
        
    return render_template('add.html', form=form)

@app.route('/payoff', methods=["POST", "GET"])
def payoff():
    form = PayoffDebt()
    if form.validate_on_submit():
        db_api = DBHelper()
        db_api.payoff_debt(form.debtor.data,
                form.creditor.data,
                form.price.data,
                form.description.data)
    return render_template('payoff.html', form=form)

@app.route('/shoplist')
def shop_list():
    db_api = DBHelper()
    persons = db_api.return_persons()
    fullname_list = []
    for person in persons:
        _id, fullname = person[0], " ".join(person[1:])
        fullname_list.append((_id, fullname))
    fullname_list = dict(fullname_list)
    results = db_api.shop_list()
    output = []
    for result in results:
        result = replacement(result, fullname_list)
        result.pop()
        output.append(result)
    return render_template('shoplist.html', output=output)

@app.route('/payofflist')
def payoff_list():
    db_api = DBHelper()
    persons = db_api.return_persons()
    fullname_list = []
    for person in persons:
        _id, fullname = person[0], " ".join(person[1:])
        fullname_list.append((_id, fullname))
    fullname_list = dict(fullname_list)
    results = db_api.payoff_list()
    output = []
    for result in results:
        result = replacement(result, fullname_list)
        result.pop()
        output.append(result)
    return render_template('payofflist.html', output=output)

@app.route('/about')
def about():
    return render_template('about.html')
