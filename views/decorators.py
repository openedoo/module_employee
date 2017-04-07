from functools import wraps
from flask import g, flash, url_for
from openedoo.core.libs import session, redirect
from modules.module_employee.models import Employee
from .API import SiteSetting


def setup_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        """Checks if there is any employee or not"""
        employee = Employee.check_records()
        if not employee:
            flash("You don't have administrator. Register one now.")
            return redirect(url_for('module_employee.setup'))
        return f(*args, **kwargs)
    return wrap


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        """Checks user is logged in or not in the session"""
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


def site_setting(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'school') or g.school is None:
            g.school = {'name': ''}
            school = SiteSetting()
            schoolData = school.get_data()
            if schoolData:
                g.school = schoolData
        return f(*args, **kwargs)
    return decorated_function
