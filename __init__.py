import datetime
from flask import flash, url_for
from openedoo_project import db
from openedoo.core.libs import (Blueprint, render_template, request, redirect,
                                session)
from openedoo.core.libs.tools import (hashing_werkzeug, check_werkzeug,
                                      session_encode)
from .views import login_required
from .forms import (LoginForm, AddEmployeeForm, EditEmployeeForm, flash_errors,
                    AssignAsTeacherForm, AddSubjectForm)
from .models import User, Teacher, Subject


module_employee = Blueprint('module_employee', __name__,
                            template_folder='templates',
                            static_folder='static')


@module_employee.route('/subject/add', methods=['GET', 'POST'])
@login_required
def add_subject():
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
        subject = Subject(data)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('module_employee.dashboard'))
    else:
        flash_errors(addSubjectForm)

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('add-subject.html', form=addSubjectForm,
                            showAdminNav=showAdminNav)

@module_employee.route('/assign/<employee_id>', methods=['GET', 'POST'])
@login_required
def assign(employee_id):
    assignAsTeacherForm = AssignAsTeacherForm()
    subjects = assignAsTeacherForm.subject.choices
    isAssignAsTeacherValid = assignAsTeacherForm.validate_on_submit()

    if isAssignAsTeacherValid:
        teacherData = {
            'user_id': employee_id,
            'subject_id': request.form['subject']
        }
        createTeacher = Teacher(teacherData)
        db.session.add(createTeacher)
        db.session.commit()
        flash('Teacher Successfully added.')
        return redirect(url_for('module_employee.dashboard'))
    else:
        flash_errors(assignAsTeacherForm)

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('assign.html',
                           form=assignAsTeacherForm,
                           showAdminNav=showAdminNav,
                           subjects=subjects,
                           employee_id=employee_id)


@module_employee.route('/', methods=['GET'])
@login_required
def dashboard():
    employees = User.query.all()
    db.session.close()

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('dashboard.html',
                           data=employees,
                           showAdminNav=showAdminNav)


@module_employee.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    validateForm = loginForm.validate_on_submit()
    if validateForm:
        username = request.form['username']
        password = request.form['password']
        employee = User.query.filter_by(username=username).first()
        db.session.close()
        if employee and check_werkzeug(employee.password, password):
            encodedSession = session_encode(employee.username)
            session['username'] = encodedSession
            return redirect(url_for('module_employee.dashboard'))
        flash('Username or password did not match.')
    else:
        flash_errors(loginForm)

    return render_template('login.html', form=loginForm)


@module_employee.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    addEmployee = AddEmployeeForm()
    isAddEmployeeValid = addEmployee.validate_on_submit()
    if isAddEmployeeValid:
        employee = {
            'username': request.form['username'],
            'fullname': request.form['fullname'],
            'password': hashing_werkzeug(request.form['password']),
            'nip': request.form['nip'],
            'created': datetime.datetime.now()
        }
        employeeData = User(employee)
        db.session.add(employeeData)
        db.session.commit()
        db.session.close()
        flash('Employee Successfully added.')
        return redirect(url_for('module_employee.dashboard'))
    else:
        flash_errors(addEmployee)

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('add-employee.html',
                           form=addEmployee,
                           showAdminNav=showAdminNav)


@module_employee.route('/edit/<employee_id>', methods=['GET', 'POST'])
@login_required
def edit(employee_id):
    employee = db.session.query(User).get(employee_id)
    editEmployee = EditEmployeeForm(employee)
    isEditEmployeeValid = editEmployee.validate_on_submit()
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

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('edit.html',
                           data=employee,
                           form=editEmployee,
                           showAdminNav=showAdminNav)


@module_employee.route('/delete/<employee_id>', methods=['GET'])
@login_required
def delete(employee_id):
    User.query.filter_by(id=employee_id).delete()
    db.session.commit()
    db.session.close()
    flash('Successfully deleted.')
    return redirect(url_for('module_employee.dashboard'))


@module_employee.route('/logout', methods=['GET'])
@login_required
def logout():
    session['username'] = False
    return render_template('logout.html')


@module_employee.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    keyword = request.form['keyword']
    employees = User.query.filter(User.fullname.like("%"+keyword+"%")).all()

    # A flag to show admin menu in the navigation bar
    showAdminNav = True
    return render_template('dashboard.html',
                           data=employees,
                           showAdminNav=showAdminNav)
