from flask import g, flash
from flask.views import View
from openedoo.core.libs import (Blueprint, render_template, request, redirect,
                                session)
from openedoo.core.libs.tools import (hashing_werkzeug, check_werkzeug,
                                      session_encode)
from modules.module_employee.forms import LoginForm, flash_errors
from modules.module_employee import models as model
from .decorators import site_setting

#: Controllers
#:
#: This controllers is based on Flask pluggable view


class Employee(View):

    methods = []
    decorators = []

    def is_form_valid(self, form):
        return form.validate_on_submit()

    def dispatch_request(self, form):
        pass


class Login(Employee):

    methods = ['GET', 'POST']
    decorators = [site_setting]

    def get_site_data(self):
        return g.school

    def dispatch_request(self):
        loginForm = LoginForm()
        isFormValid = self.is_form_valid(loginForm)
        if isFormValid:
            username = request.form['username']
            password = request.form['password']
            employee = model.Employee.filter_by(username=username).first()
            if employee and check_werkzeug(employee.password, password):
                encodeUsername = session_encode(employee.username)
                session['username'] = encodeUsername
                return redirect(url_for('module_employee.dashboard'))
            flash(u'Username or password did not match.', 'error')
        flash_errors(loginForm)
        return render_template('admin/login.html',
                               school=self.get_site_data(),
                               form=loginForm)
