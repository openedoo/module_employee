import datetime
from functools import wraps
from openedoo.core.libs import (render_template, redirect, request,
                                session, blueprint)
from openedoo.core.libs.tools import session_encode
from openedoo import app, db
from database import User
from flask import jsonify, flash, url_for
from faker import Faker
from .forms import Login


module_employee = blueprint('module_employee', __name__,
                            template_folder='templates',
                            static_folder='static')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        session.permanent = True
        try:
            if session['username'] is False:
                flash('You must login first!')
                return redirect(url_for('module_employee.login'))
            return f(*args, **kwargs)
        except KeyError:
            flash('Your session is timeout!')
            return redirect(url_for('module_employee.login'))
    return wrap


@module_employee.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = Login()
    if loginForm.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        employee = User.query.filter_by(username=username).first()
        if employee.password == password:
            encodedSession = session_encode(employee.username)
            session['username'] = encodedSession
            return redirect(url_for('module_employee.employees'))
        flash('Username or password did not match.')
        return redirect(url_for('module_employee.login'))
    return render_template('login.html', form=loginForm)


@module_employee.route('/insert', methods=['GET'])
def index():
    """Generates Fake data to database"""
    try:
        fake = Faker()
        data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'fullname': fake.name(),
            'access_token': 'glakhgaie837w9',
            'public_key': 'asdalksjd',
            'private_key': 'asde',
            'status': 0,
            'role': 't',
            'created': datetime.datetime.now(),
            'last_login': datetime.datetime.now(),
            'nip': fake.random_digit_not_null()
        }
        fakeUser = User(data)
        db.session.add(fakeUser)
        db.session.commit()
        return 'Fake User added'
    except Exception as e:
        message = {'error': str(e)}
        return jsonify(message)


@module_employee.route('/employees', methods=['GET'])
@login_required
def employees():
    print session['username']
    return jsonify([i.serialize for i in User.query.all()])


@module_employee.route('/logout', methods=['GET'])
@login_required
def logout():
    session['username'] = False
    return render_template('logout-page.html')
