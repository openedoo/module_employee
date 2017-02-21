import datetime
from openedoo.core.libs import (render_template, redirect, request,
                                session, blueprint)
from openedoo import db
from database import User
from flask import jsonify
from faker import Faker
from .forms import Login


module_employee = blueprint('module_employee', __name__,
                            template_folder='templates',
                            static_folder='static')


@module_employee.route('/', methods=['GET', 'POST'])
def home():
    login = Login()
    if login.validate_on_submit():
        redirect(url_for('employees'))
    return render_template('login-page.html', form=login)


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


@module_employee.route('/API/0.1/employees', methods=['GET'])
def employees():
    return jsonify([i.serialize for i in User.query.all()])
