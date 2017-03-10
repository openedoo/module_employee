import datetime
from functools import wraps
from openedoo.core.libs import (render_template, redirect, request,
                                session, blueprint)
from openedoo.core.libs.tools import (session_encode, hashing_werkzeug,
                                      check_werkzeug)
from openedoo import app, db
from .models import User
from .forms import (flash_errors, LoginForm,
                    EditEmployeeForm, AddEmployeeForm)
from flask import jsonify, flash, url_for


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
    employees = User.query.all()
    db.session.close()

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('dashboard.html',
                           data=employees,
                           showAdminNav=showAdminNav)


@module_employee.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    validateForm = loginForm.validate_on_submit()
    if validateForm:
        username = request.form['username']
        password = request.form['password']
        employee = User.query.filter_by(username=username).first()
        db.session.close()
        if employee and check_werkzeug(employee.password, password):
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
    addEmployee = AddEmployeeForm()
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

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('add-employee.html',
                           form=addEmployee,
                           showAdminNav=showAdminNav)


@module_employee.route('/edit/<employee_id>', methods=['GET', 'POST'])
@login_required
def edit(employee_id):
    employee = db.session.query(User).get(employee_id)
    editEmployee = EditEmployeeForm(employee)
    isEditEmployeeValid = editEmployee.validate_on_submit()
    if isEditEmployeeValid:
        employee.username = request.form['username']
        employee.fullname = request.form['fullname']
        employee.nip = request.form['nip']
        db.session.commit()
        flash('Successfully updated.!')
        url = url_for('module_employee.edit', employee_id=employee.id)
        return redirect(url)
    else:
        flash_errors(editEmployee)

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('edit.html',
                           data=employee,
                           form=editEmployee,
                           showAdminNav=showAdminNav)


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


@module_employee.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    keyword = request.form['keyword']
    employees = User.query.filter(User.fullname.like("%"+keyword+"%")).all()

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('dashboard.html',
                           data=employees,
                           showAdminNav=showAdminNav)
