import datetime
from functools import wraps
from openedoo.core.libs import (render_template, redirect, request,
                                session, blueprint)
from openedoo.core.libs.tools import (session_encode, hashing_werkzeug,
                                      check_werkzeug)
from openedoo import app, db
from database import User
from flask import jsonify, flash, url_for
from .forms import Login, AddEmployee, flash_errors


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
    db.session.close()
    return render_template('dashboard.html', data=employees)


@module_employee.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = Login()
    validateForm = loginForm.validate_on_submit()
    if validateForm:
        username = request.form['username']
        password = request.form['password']
        employee = User.query.filter_by(username=username).first()
        db.session.close()
        if check_werkzeug(employee.password, password):
            encodedSession = session_encode(employee.username)
            session['username'] = encodedSession
            return redirect(url_for('module_employee.dashboard'))
        flash('Username or password did not match.')
    else:
        flash_errors(loginForm)

    return render_template('login.html', form=loginForm)


@module_employee.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    addEmployee = AddEmployee()
    isAddEmployeeValid = addEmployee.validate_on_submit()
    if isAddEmployeeValid:
        employee = {
            'username': request.form['username'],
            'fullname': request.form['fullname'],
            'password': hashing_werkzeug(request.form['password']),
            'nip': request.form['nip'],
            'role': 'employee',
            'created': datetime.datetime.now()
        }
        employeeData = User(employee)
        db.session.add(employeeData)
        db.session.commit()
        db.session.close()
        flash('Employee Successfully added.')
        return redirect(url_for('module_employee.dashboard'))
    else:
        flash_errors(addEmployee)
    return render_template('add-employee.html', form=addEmployee)


@module_employee.route('/edit/<employee_id>', methods=['GET', 'POST'])
@login_required
def edit(employee_id):
    """Shows existing data,
    The Update process is not yet implemented
    """
    employee = db.session.query(User).get(employee_id)
    return render_template('edit.html', data=employee)


@module_employee.route('/delete/<employee_id>', methods=['GET'])
@login_required
def delete(employee_id):
    User.query.filter_by(id=employee_id).delete()
    db.session.commit()
    db.session.close()
    flash('Successfully deleted.')
    return redirect(url_for('module_employee.dashboard'))


@module_employee.route('/logout', methods=['GET'])
@login_required
def logout():
    session['username'] = False
    return render_template('logout.html')
