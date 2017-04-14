import unittest
from flask import url_for
from openedoo_project import app, db


class Employee(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        self.superuser = {
            'username': 'dwip',
            'password': 'asdzxcfv'
        }

    def tearDown(self):
        self.app_context.pop()

    def test_unittest_can_detect_this_test(self):
        response = self.client.get(url_for('module_employee.login'))
        partOfThePage = '<form class=\"form\" method=\"post\" action=\"/employee/admin/login\">'
        self.assertTrue(partOfThePage in response.get_data(as_text=True))

    def test_restricted_page(self):
        # Redirect to login page when not logged in
        dashboard = self.client.get(url_for('module_employee.dashboard'))
        self.assertTrue(dashboard.status_code == 302)

        # Unregistered employee cannot login
        partOfThePage = 'Username or password did not match.'
        login = self.client.post(url_for('module_employee.login'), data={
            'username': 'andika',
            'password': '1231231nfansdas'
        }, follow_redirects=True)
        self.assertTrue(partOfThePage in login.get_data(as_text=True))

        # Superuser employee can login
        partOfThePage = '<div class=\"main-dashboard container\">'
        login = self.client.post(url_for('module_employee.login'),
                                 data=self.superuser,
                                 follow_redirects=True)
        self.assertTrue(partOfThePage in login.get_data(as_text=True))

        # Superuser employee is succesfully logged out
        partOfThePage = 'Successfully logged out, good bye!'
        logout = self.client.get(url_for('module_employee.logout'),
                                 follow_redirects=True)
        self.assertTrue(partOfThePage in logout.get_data(as_text=True))

    def test_employee_adds_subject(self):
        # Employee login
        partOfTheDashboard = '<div class=\"main-dashboard container\">'
        login = self.client.post(url_for('module_employee.login'),
                                 data=self.superuser,
                                 follow_redirects=True)
        self.assertTrue(partOfTheDashboard in login.get_data(as_text=True))

        # Get add subject page
        partOfThePage = '<h3 class=\"text-center\">Add Subject Information</h3>'
        addSubject = self.client.get(url_for('module_employee.add_subject'),
                                     follow_redirects=True)
        self.assertTrue(partOfThePage in addSubject.get_data(as_text=True))

        # Subject is succesfully added
        subjectData = {
            'code': 'MK654',
            'name': 'Matematika I',
            'major': 'IPA',
            'grade': 11,
            'weight': '4',
            'category': 'wajib',
            'curriculum': 1999,
            'alias': ''
        }
        subject = self.client.post(url_for('module_employee.add_subject'),
                                   data=subjectData)
        self.assertTrue(subject.status_code == 302)
