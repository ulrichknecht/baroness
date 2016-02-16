from check_rights import *
from flask import render_template, request, redirect, session, send_from_directory
from app import app
from database import *
from plot import *
from user import User
from product import Product
from consumption import Consumption



@app.route('/static/<path:path>')
def static_proxy(path):
    return send_from_directory('./static/', path)


@app.route('/')
@app.route('/index')
def index():
    consumed = get_consumed()
    plot_total()
    plot_list(4)
    #generate_test_users()
    #generate_test_consumptions()
    return render_template("index.html", consumed=consumed, user=get_user_by_name(session.get('name')))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if 'name' in session: #check if usr is already logged in
        return redirect('/')

    if request.method == 'POST':
        u = User()
        u.name = request.form['username'].lower()

        u = get_user(u)

        if u is None:
            error = 'User does not exist!'
            return render_template('login.html', error=error, user=get_user_by_name(session.get('name')))
        if u.password != request.form['password']:
            error = 'Wrong password!'
            return render_template('login.html', error=error, user=get_user_by_name(session.get('name')))

        session['name'] = u.name
        return redirect('/')

    return render_template('login.html', error=error, user=get_user_by_name(session.get('name')))


@app.route('/logout')
@requires_login
def logout():
    session.pop('name', None)
    return redirect('/')


@app.route('/manage_users')
@requires_baron
def manage_users():
    users = get_users()
    return render_template('manage_users.html', users=users, user=get_user_by_name(session.get('name')))


@app.route('/manage_users/add', methods=['POST', 'GET'])
@requires_baron
def manage_users_add():
    if request.method == 'POST':
        u = User()
        error = None
        u.name = request.form['username'].lower()
        if u.name is None:
            error = "Username not unique!"

        if request.form['password1'] == request.form['password2']:
            u.password = request.form['password1']        	
        else:
            error="Passwords do not match!"
        u.longname=request.form['longname']
        u.email = request.form['email']
        u.rfid_id = request.form['rfid_id']

        if error is None:
            add_user(u)
            return render_template('manage_users_add.html', success="User created!", user=get_user_by_name(session.get('name')));

        return render_template('manage_users_add.html', error=error, user=get_user_by_name(session.get('name')))
    return render_template('manage_users_add.html', user=get_user_by_name(session.get('name')))


@app.route('/manage_users/edit', methods=['POST'])
@app.route('/manage_users/edit/<name>', methods=['GET'])
@requires_baron
def manage_users_edit(name=None):
    if request.method == 'GET':
        error = None
        u = User()
        u.name = name
        u = get_user(u)

        if u is None:
            error = "User existiert nicht"

        return render_template('manage_users_edit.html', user_to_edit=u, error=error, user=get_user_by_name(session.get('name')))

    if request.method == 'POST':
        u = User()
        #print request.form
        u.id = request.form['id']
        u.name = request.form['username'].lower()
        u.longname=request.form['longname']
        u.email = request.form['email']
        u.rfid_id = request.form['rfid_id']

        if 'isblack' in request.form:
            u.isblack = True
        else:
            u.isblack = False

        if 'isbaron' in request.form:
            u.isbaron = True
        else:
            u.isbaron = False

        if 'isshown' in request.form:
            u.isshown = True
        else:
            u.isshown = False

        update_user(u)

        return redirect('/manage_users')


@app.route('/manage_beverages')
@requires_baron
def manage_beverages():
    products = get_products()
    return render_template('manage_beverages.html', products=products, user=get_user_by_name(session.get('name')))


@app.route('/manage_beverages/edit', methods=['POST'])
@app.route('/manage_beverages/edit/<name>', methods=['GET'])
@requires_baron
def manage_beverages_edit(name=None):
    if request.method == 'GET':
        error = None
        p = get_product_by_name(name);

        if p is None:
            error = "Product existiert nicht"

        return render_template('manage_beverages_edit.html', product_to_edit=p, error=error, user=get_user_by_name(session.get('name')))

    if request.method == 'POST':
        p = Product()
        #print request.form
        p.id = request.form['id']
        p.name = request.form['name']
        p.price = float(request.form['price'])

        if 'isshown' in request.form:
            p.isshown = True
        else:
            p.isshown = False

        update_product(p)

        # update_user(u)

        return redirect('/manage_beverages')


@app.route('/manage_beverages/add', methods=['POST', 'GET'])
@requires_baron
def manage_beverages_add():
    if request.method == 'POST':
        p = Product()
        error = None
        print request
        p.name = request.form['name']
        #if request.form['price'].isnumeric():
        p.price = float(request.form['price'])
        #else:
        #    error = "Preis muss eine Nummer sein."

        if 'isshown' in request.form:
            p.isshown = True
        else:
            p.isshown = False

        if error is None:
            add_product(p)
            return render_template('manage_beverages_add.html', success="Konsumat hinzugefuegt.", user=get_user_by_name(session.get('name')))

        return render_template('manage_beverages_add.html', error=error, user=get_user_by_name(session.get('name')))
    return render_template('manage_beverages_add.html', user=get_user_by_name(session.get('name')))


@app.route('/consume')
@requires_login
def consume():
    products = get_products()
    message = []
    prodid = request.args.get('prodid')
    if prodid is not None:
        prod = get_product_by_id(prodid)
        username = session.get('name')
        add_consume(username, prod.id)
        message = "Du hast gerade ein %s konsumiert." % prod.name
        plot_total(get_user_by_name(session.get('name')))
        plot_total()
    return render_template('consume.html', products=products, message=message, user=get_user_by_name(session.get('name')))

@app.route('/billing')
@requires_baron
def billing():

    return render_template('billing.html', user=get_user_by_name(session.get('name')))
