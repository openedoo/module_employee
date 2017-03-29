from openedoo_project import db
from openedoo_project import config

database_prefix = config.database_prefix


class Subject(db.Model):
    __tablename__ = '{db_prefix}_subject'.format(db_prefix=database_prefix)
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(80))
    name = db.Column(db.Text())
    major = db.Column(db.String(6), nullable=True)
    grade = db.Column(db.Integer)
    weight = db.Column(db.String(4))
    category = db.Column(db.String(8))
    curriculum = db.Column(db.Integer)
    alias = db.Column(db.Text)

    def __init__(self, data={}):
        if data is None:
            raise ValueError('Subject is supplied with wrong data!')

        self.code = data['code']
        self.name = data['name']
        self.major = data['major']
        self.grade = data['grade']
        self.weight = data['weight']
        self.category = data['category']
        self.curriculum = data['curriculum']
        self.alias = data['alias']
