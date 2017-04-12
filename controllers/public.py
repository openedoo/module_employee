from openedoo.core.libs import render_template
from modules.module_employee import models
from modules.module_employee.views.decorators import site_setting, setup_required
from .base_controller import BaseController


class EmployeeList(BaseController):

    methods = ['GET']
    decorators = [site_setting, setup_required]

    def dispatch_request(self):
        employees = models.Employee.get_public_list()
        return render_template('module_employee/public/list.html',
                               data=employees,
                               school=self.get_site_data())
