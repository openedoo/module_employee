from openedoo.core.libs import render_template
from modules.module_employee import models
from modules.module_employee.views.decorators import site_setting
from .base_controller import BaseController


class EmployeeList(BaseController):

    methods = ['GET']
    decorators = [site_setting]

    def dispatch_request(self):
        employees = models.Employee.get_public_list()
        return render_template('public/list.html',
                               data=employees,
                               school=self.get_site_data())
