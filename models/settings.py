from openedoo_project import db


class Setting(db.Model):
    __tablename__ = 'module_employee_site_setting'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def insert(self, data=None):
        self.name = data['name']
        db.session.add(self)
        return db.session.commit()

    def get_existing_name(self):
        setting = self.query.limit(1).first()
        return setting

    def update(self, data):
        setting = self.get_existing_name()
        setting.name = data['name']
        return db.session.commit()
