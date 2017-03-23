from openedoo_project import db
from openedoo_project import config


class Setting(db.Model):
    __tablename__ = 'module_employee_site_setting'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
