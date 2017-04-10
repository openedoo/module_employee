from openedoo_project import db
from openedoo.core.libs import Blueprint
from .controllers.employee import EmployeeLogin, EmployeeLogout, AddEmployee, \
    AssignEmployeeAsTeacher, EmployeeDashboard, EditEmployee, DeleteEmployee, \
    SearchEmployee, AddSubject, EmployeeSetup
from .controllers.site_setting import SiteSetting
from .controllers.public import EmployeeList


module_employee = Blueprint('module_employee', __name__,
                            template_folder='templates',
                            static_folder='static')


module_employee.add_url_rule('/', view_func=EmployeeList.as_view('public_list'))
module_employee.add_url_rule('/setup', view_func=EmployeeSetup.as_view('setup'))
module_employee.add_url_rule('/admin',
                             view_func=EmployeeDashboard.as_view('dashboard'))
module_employee.add_url_rule('/admin/login',
                             view_func=EmployeeLogin.as_view('login'))
module_employee.add_url_rule('/admin/logout',
                             view_func=EmployeeLogout.as_view('logout'))
module_employee.add_url_rule('/admin/add',
                             view_func=AddEmployee.as_view('add'))
module_employee.add_url_rule('/admin/edit',
                             view_func=EditEmployee.as_view('edit'))
assignEmployeeAsTeacherView = AssignEmployeeAsTeacher.as_view('assign')
module_employee.add_url_rule('/admin/assign',
                             view_func=assignEmployeeAsTeacherView)
module_employee.add_url_rule('/admin/delete',
                             view_func=DeleteEmployee.as_view('delete'))
module_employee.add_url_rule('/admin/setting',
                             view_func=SiteSetting.as_view('setting'))
module_employee.add_url_rule('/search',
                             view_func=SearchEmployee.as_view('search'))
module_employee.add_url_rule('/admin/subject/add',
                             view_func=AddSubject.as_view('add_subject'))
