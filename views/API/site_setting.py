from flask import json
from modules.module_employee.models import Setting


class SiteSetting():
    def get_data(self):
        setting = Setting.query.first()
        if setting:
            return setting.serialize()
        return False

    def make_response(self):
        return json.jsonify(self.get_data())
