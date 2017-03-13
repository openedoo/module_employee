from openedoo import db
from openedoo import config

database_prefix = config.database_prefix


class Subject(db.Model):
    __tablename__ = '{db_prefix}_subject'.format(db_prefix=database_prefix)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(80))
    name = db.Column(db.Text())
    major = db.Column(db.String(6), nullable=True)
    grade = db.Column(db.Integer)
    weight = db.Column(db.String(4))
    category = db.Column(db.String(8))
    curriculum = db.Column(db.Integer)
    alias = db.Column(db.Text)
