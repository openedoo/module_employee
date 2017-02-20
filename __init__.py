import datetime
from openedoo.core.libs import blueprint
from openedoo import db
from database import User
from flask import jsonify, render_template
from faker import Faker

fake = Faker()

module_employee = blueprint('module_employee', __name__,
                            template_folder='templates',
                            static_folder='static')


@module_employee.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@module_employee.route('/insert', methods=['GET'])
def index():
    """Generates Fake data to database"""
    try:
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
        paimin = User(data)
        db.session.add(paimin)
        db.session.commit()
        return 'ko'
    except Exception as e:
        message = {'error': str(e)}
        return jsonify(message)


@module_employee.route('/API/0.1/employees', methods=['GET'])
def employees():
    return jsonify([i.serialize for i in User.query.all()])
