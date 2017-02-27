import datetime
from functools import wraps
from openedoo.core.libs import (render_template, redirect, request,
                                session, blueprint)
from openedoo.core.libs.tools import (session_encode, hashing_werkzeug,
                                      check_werkzeug)
from openedoo import app, db
from database import User
from flask import jsonify, flash, url_for
from .forms import Login, flash_errors


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


@module_employee.route('/', methods=['GET'])
@login_required
def dashboard():
    employees = User.query.limit(5).all()
    return render_template('dashboard.html', data=employees)


@module_employee.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = Login()
    reqMethod = request.method
    validateForm = loginForm.validate_on_submit()
    if validateForm:
        username = request.form['username']
        password = request.form['password']
        employee = User.query.filter_by(username=username).first()
        if check_werkzeug(employee.password, password):
            encodedSession = session_encode(employee.username)
            session['username'] = encodedSession
            return redirect(url_for('module_employee.dashboard'))
        flash('Username or password did not match.')
    else:
        flash_errors(loginForm)

    return render_template('login.html', form=loginForm)


@module_employee.route('/employees', methods=['GET'])
@login_required
def employees():
    print session['username']
    return jsonify([i.serialize for i in User.query.all()])


@module_employee.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    return render_template('add-employee.html')


@module_employee.route('/logout', methods=['GET'])
@login_required
def logout():
    session['username'] = False
    return render_template('logout.html')
