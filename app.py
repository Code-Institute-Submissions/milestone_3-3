import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if os.path.exists('env.py'):
    import env

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'milestone-3'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_users')
def get_users():
    """
    VIEWING USERS AS USER
    """

    return render_template('users.html', users=mongo.db.users.find())


@app.route('/users_admin')
def users_admin():
    """
    VIEWING ALL PERMITS AS USER
    """

    return render_template('users_admin.html',
                           users=mongo.db.users.find().sort('last_name'
                           ))


@app.route('/new_user')
def new_user():
    """
    RENDER NEW USER FORM
    """

    return render_template('new_user.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    """
    ADDING NEW USER
    """

    users = mongo.db.users
    users.insert(request.form.to_dict())
    return render_template('users.html', users=mongo.db.users.find())


@app.route('/delete_user/<users_id>')
def delete_user(users_id):
    """
    DELETING USERS AS ADMIN
    """

    mongo.db.users.remove({'_id': ObjectId(users_id)})
    return render_template('users_admin.html',
                           users=mongo.db.users.find().sort('last_name'
                           ))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """
    ADMIN LOGIN
    """

    error = None
    if request.method == 'POST':
        if request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('permits_admin'))
    return render_template('admin_login.html', error=error)


@app.route('/login/<users_id>', methods=['GET', 'POST'])
def login(users_id):
    """
    USER LOGIN
    """

    error = None
    the_users = mongo.db.users.find_one({'_id': ObjectId(users_id)})
    if request.method == 'POST':
        if request.form['password'] != the_users['password']:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('permits'))
    return render_template('login.html', error=error, user=the_users)


@app.route('/permits')
def permits():
    """
    VIEWING ALL PERMITS AS USER
    """

    return render_template('permits.html',
                           permits=mongo.db.permits.find().sort('date'))


@app.route('/permits_admin')
def permits_admin():
    """
    VIEWING ALL PERMITS AS ADMIN
    """

    return render_template('permits_admin.html',
                           permits=mongo.db.permits.find().sort('date'))


@app.route('/new_permit')
def new_permit():
    """
    RENDER NEW PERMIT FORM
    """

    return render_template('new_permit.html')


@app.route('/add_permit', methods=['POST'])
def add_permit():
    """
    ADDING NEW PERMIT
    """

    permits = mongo.db.permits
    permits.insert(request.form.to_dict())
    return render_template('permits.html',
                           permits=mongo.db.permits.find().sort('date'))


@app.route('/edit_permit/<permits_id>')
def edit_permit(permits_id):
    """
    EDITING PERMIT
    """

    the_permits = \
        mongo.db.permits.find_one({'_id': ObjectId(permits_id)})
    return render_template('edit_permit.html', permit=the_permits)


@app.route('/update_permit/<permits_id>', methods=['POST'])
def update_permit(permits_id):
    """
    UPDATING PERMIT
    """

    permits = mongo.db.permits
    permits.update({'_id': ObjectId(permits_id)}, {
        'date': request.form.get('date'),
        'crew_size': request.form.get('crew_size'),
        'location': request.form.get('location'),
        'supervisor': request.form.get('supervisor'),
        'request_by': request.form.get('request_by'),
        'contractor': request.form.get('contractor'),
        'sub_contractor': request.form.get('sub_contractor'),
        'work_description': request.form.get('work_description'),
        'system_name': request.form.get('system_name'),
        'system_number': request.form.get('system_number'),
        'equipment_tools': request.form.get('equipment_tools'),
        'method': request.form.get('method'),
        'risk': request.form.get('risk'),
        'spa': request.form.get('spa'),
        'excavation': request.form.get('excavation'),
        'scanned': request.form.get('scanned'),
        'shored': request.form.get('shored'),
        'battered': request.form.get('battered'),
        'skills_card': request.form.get('skills_card'),
        'confined_space': request.form.get('confined_space'),
        'atmosphere': request.form.get('atmosphere'),
        'trained_persons': request.form.get('trained_persons'),
        'emerg_o2': request.form.get('emerg_o2'),
        'elec_works': request.form.get('elec_works'),
        'locks': request.form.get('locks'),
        'persons_locks': request.form.get('persons_locks'),
        'energy_released': request.form.get('energy_released'),
        'hazards': request.form.get('hazards'),
        })
    return render_template('permits.html',
                           permits=mongo.db.permits.find().sort('date'))


@app.route('/view_permit/<permits_id>')
def view_permit(permits_id):
    """
    VIEWING INDIVIDUAL PERMITS AS USER
    """

    the_permits = \
        mongo.db.permits.find_one({'_id': ObjectId(permits_id)})
    return render_template('view_permit.html', permit=the_permits)


@app.route('/view_permit_admin/<permits_id>')
def view_permit_admin(permits_id):
    """
    VIEWING INDIVIDUAL PERMITS AS ADMIN
    """

    the_permits = \
        mongo.db.permits.find_one({'_id': ObjectId(permits_id)})
    return render_template('view_permit_admin.html', permit=the_permits)


@app.route('/delete_permit/<permits_id>')
def delete_permit(permits_id):
    """
    DELETING PERMITS AS ADMIN
    """

    mongo.db.permits.remove({'_id': ObjectId(permits_id)})
    return render_template('permits_admin.html',
                           permits=mongo.db.permits.find().sort('date'))

if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=False)