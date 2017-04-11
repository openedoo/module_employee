import datetime
from openedoo.core.libs.tools import hashing_werkzeug
from openedoo_project import db
from .users import User


class Employee(User):

    @classmethod
    def is_exist(self, username):
        employee = self.query.get(username=username).first()
        return employee

    @classmethod
    def get_public_list(self):
        employees = self.query.with_entities(self.username,
                                             self.fullname,
                                             self.nip)
        return employees

    @classmethod
    def check_records(self):
        employees = self.query.limit(1).all()
        return employees

    @classmethod
    def add(self, form={}):
        if not form:
            raise ValueError('Form is supplied with wrong data.')

        data = {
            'username': form['username'],
            'fullname': form['fullname'],
            'password': hashing_werkzeug(form['password']),
            'nip': form['nip'],
            'created': datetime.datetime.now()
        }
        employeeData = self(data)
        db.session.add(employeeData)
        return db.session.commit()
