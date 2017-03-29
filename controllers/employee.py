import datetime
from flask import flash, url_for
from openedoo.core.libs import (render_template, request, redirect, session)
from openedoo.core.libs.tools import (hashing_werkzeug, check_werkzeug,
                                      session_encode)
from openedoo_project import db
from modules.module_employee.forms import LoginForm, AddEmployeeForm, \
    flash_errors
from modules.module_employee.views.decorators import site_setting, \
    login_required
from modules.module_employee import models as model
from .base_controller import BaseController


class EmployeeLogin(BaseController):
    """Employee login controller."""

    methods = ['GET', 'POST']
    decorators = [site_setting]

    def dispatch_request(self):
        loginForm = LoginForm()
        isFormValid = self.is_form_valid(loginForm)
        if isFormValid:
            username = request.form['username']
            password = request.form['password']
            employees = model.Employee.query.filter_by(username=username)
            employee = employees.first()
            if employee and check_werkzeug(employee.password, password):
                encodeUsername = session_encode(employee.username)
                session['username'] = encodeUsername
                return redirect(url_for('module_employee.dashboard'))
            flash(u'Username or password did not match.', 'error')
        flash_errors(loginForm)
        return render_template('admin/login.html',
                               school=self.get_site_data(),
                               form=loginForm)


class EmployeeLogout(BaseController):
    """Employee logout controller."""

    methods = ['GET']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        session['username'] = False
        return render_template('admin/logout.html',
                               school=self.get_site_data())


class AddEmployee(BaseController):
    """Add employee controller.

    A new employee can only be added by existing employee.
    """

    methods = ['GET', 'POST']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        addEmployeeForm = AddEmployeeForm()
        isAddEmployeeValid = self.is_form_valid(addEmployeeForm)
        if isAddEmployeeValid:
            data = {
                'username': request.form['username'],
                'fullname': request.form['fullname'],
                'password': hashing_werkzeug(request.form['password']),
                'nip': request.form['nip'],
                'created': datetime.datetime.now()
            }
            employeeData = model.Employee(data)
            db.session.add(employeeData)
            db.session.commit()
            flash(u'Employee Successfully Added.')
            return redirect(url_for('module_employee.dashboard'))
        else:
            flash_errors(addEmployeeForm)

        # A flag to show admin in the navigation bar
        showAdminNav = True
        return render_template('admin/add-employee.html',
                               form=addEmployeeForm,
                               school=self.get_site_data(),
                               showAdminNav=showAdminNav)
