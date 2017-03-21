from openedoo_project import db
from openedoo_project import config
from .users import User
from .subjects import Subject

database_prefix = config.database_prefix


class Teacher(db.Model):
    __tablename__ = '{db_prefix}_teacher'.format(db_prefix=database_prefix)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id))

    def __init__(self, data={}):
        self.user_id = data['user_id']
        self.subject_id = data['subject_id']
