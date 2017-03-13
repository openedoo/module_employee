from openedoo import db
from openedoo import config
from .users import User
from .subjects import Subject

database_prefix = config.database_prefix


class Teacher(db.Model):
    __tablename__ = '{db_prefix}_teacher'.format(db_prefix=database_prefix)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(User.id, ondelete='CASCADE'),
                        nullable=False)
    subject_id = db.Column(db.Integer,
                           db.ForeignKey(Subject.id, ondelete='CASCADE'))
