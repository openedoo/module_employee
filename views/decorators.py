from functools import wraps
from flask import g, flash, url_for
from openedoo.core.libs import session, redirect
from .API import SiteSetting


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
            school = SiteSetting()
            g.school = school.get_data()
        return f(*args, **kwargs)
    return decorated_function
