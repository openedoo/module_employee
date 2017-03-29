import datetime
from flask import flash, url_for
from openedoo.core.libs import (render_template, request, redirect, session)
from openedoo.core.libs.tools import (hashing_werkzeug, check_werkzeug,
                                      session_encode)
from openedoo_project import db
from modules.module_employee.forms import LoginForm, AddEmployeeForm, \
    AssignAsTeacherForm, EditEmployeeForm, AddSubjectForm, flash_errors
from modules.module_employee.views.decorators import site_setting, \
    login_required
from modules.module_employee import models as model
from .base_controller import BaseController


class EmployeeLogin(BaseController):
    """Employee login controller."""

    methods = ['GET', 'POST']
    decorators = [site_setting]

    def dispatch_request(self):
        loginForm = LoginForm()
        isFormValid = self.is_form_valid(loginForm)
        if isFormValid:
            username = request.form['username']
            password = request.form['password']
            employees = model.Employee.query.filter_by(username=username)
            employee = employees.first()
            if employee and check_werkzeug(employee.password, password):
                encodeUsername = session_encode(employee.username)
                session['username'] = encodeUsername
                return redirect(url_for('module_employee.dashboard'))
            flash(u'Username or password did not match.', 'error')
        flash_errors(loginForm)
        return render_template('admin/login.html',
                               school=self.get_site_data(),
                               form=loginForm)


class EmployeeLogout(BaseController):
    """Employee logout controller."""

    methods = ['GET']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        session['username'] = False
        return render_template('admin/logout.html',
                               school=self.get_site_data())


class AddEmployee(BaseController):
    """Add employee controller.

    A new employee can only be added by existing employee.
    """

    methods = ['GET', 'POST']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        addEmployeeForm = AddEmployeeForm()
        isAddEmployeeValid = self.is_form_valid(addEmployeeForm)
        if isAddEmployeeValid:
            data = {
                'username': request.form['username'],
                'fullname': request.form['fullname'],
                'password': hashing_werkzeug(request.form['password']),
                'nip': request.form['nip'],
                'created': datetime.datetime.now()
            }
            employeeData = model.Employee(data)
            db.session.add(employeeData)
            db.session.commit()
            flash(u'Employee Successfully Added.')
            return redirect(url_for('module_employee.dashboard'))
        else:
            flash_errors(addEmployeeForm)

        return render_template('admin/add-employee.html',
                               form=addEmployeeForm,
                               school=self.get_site_data(),
                               showAdminNav=self.show_admin_nav())


class AssignEmployeeAsTeacher(BaseController):
    """Assign employee as teacher controller."""

    methods = ['GET', 'POST']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        assignAsTeacherForm = AssignAsTeacherForm()
        subjects = assignAsTeacherForm.subject.choices
        isAssignAsTeacherValid = self.is_form_valid(assignAsTeacherForm)
        employee_id = request.args.get('employee_id')
        if isAssignAsTeacherValid:
            teacherData = {
                'user_id': employee_id,
                'subject_id': request.form['subject']
            }
            createTeacher = model.Teacher(teacherData)
            db.session.add(createTeacher)
            db.session.commit()
            flash('Teacher Successfully added.')
            return redirect(url_for('module_employee.dashboard'))
        else:
            flash_errors(assignAsTeacherForm)

        return render_template('admin/assign.html',
                               school=self.get_site_data(),
                               form=assignAsTeacherForm,
                               showAdminNav=self.show_admin_nav(),
                               subjects=subjects,
                               employee_id=employee_id)


class EmployeeDashboard(BaseController):
    """Employee dashboard controller."""

    methods = ['GET']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        employees = model.Employee.query.all()

        return render_template('admin/dashboard.html',
                               school=self.get_site_data(),
                               data=employees,
                               showAdminNav=self.show_admin_nav())


class EditEmployee(BaseController):
    """Edit employee controller."""

    methods = ['GET', 'POST']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        employee_id = request.args.get('employee_id')
        employee = model.Employee.query.filter_by(id=employee_id).first()
        editEmployee = EditEmployeeForm(employee)
        isEditEmployeeValid = self.is_form_valid(editEmployee)
        if isEditEmployeeValid:
            employee.username = request.form['username']
            employee.fullname = request.form['fullname']
            employee.nip = request.form['nip']
            db.session.commit()
            flash('Successfully updated.!')
            url = url_for('module_employee.edit', employee_id=employee.id)
            return redirect(url)
        else:
            flash_errors(editEmployee)

        return render_template('admin/edit.html',
                               school=self.get_site_data(),
                               data=employee,
                               form=editEmployee,
                               showAdminNav=self.show_admin_nav())


class DeleteEmployee(BaseController):
    """Delete employee controller."""

    methods = ['GET']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        employee_id = request.args.get('employee_id')
        model.Employee.query.filter_by(id=employee_id).delete()
        db.session.commit()
        flash('Successfully deleted.')
        return redirect(url_for('module_employee.dashboard'))


class SearchEmployee(BaseController):
    """Search employee controller."""

    methods = ['GET', 'POST']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        keyword = request.form['keyword']
        employees = model.Employee.query.filter(
            model.Employee.fullname.like("%"+keyword+"%")).all()

        return render_template('admin/dashboard.html',
                               school=self.get_site_data(),
                               data=employees,
                               showAdminNav=self.show_admin_nav())


class AddSubject(BaseController):
    """Add subject controller."""

    methods = ['GET', 'POST']
    decorators = [site_setting, login_required]

    def dispatch_request(self):
        addSubjectForm = AddSubjectForm()
        isAddSubjectFormValid = addSubjectForm.validate_on_submit()
        if isAddSubjectFormValid:
            data = {
                'code': request.form['code'],
                'name': request.form['name'],
                'major': request.form['major'],
                'grade': request.form['grade'],
                'weight': request.form['weight'],
                'category': request.form['category'],
                'curriculum': request.form['curriculum'],
                'alias': request.form['alias']
            }
            subject = model.Subject(data)
            db.session.add(subject)
            db.session.commit()
            return redirect(url_for('module_employee.dashboard'))
        else:
            flash_errors(addSubjectForm)

        return render_template('admin/add-subject.html',
                               school=self.get_site_data(),
                               form=addSubjectForm,
                               showAdminNav=self.show_admin_nav())
