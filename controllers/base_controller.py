from flask import g
from flask.views import View


class BaseController(View):
    """Base Controller

    The base controller of this module, it shows how to make
    'class based controller' with 'Flask Pluggable view'.
    You can make controller inherited from BaseController
    not from Flask.View

        class ExampleController(BaseController):
            # your methods

    """

    methods = []
    decorators = []

    def show_admin_nav(self):
        """Show admin navigation flag

        This is just a boolean flag to help admin menu in top navigation bar
        should show or not.

        TODO: Make better implementation that show/hide admin menu
        """
        return True

    def is_form_valid(self, form):
        """Validate form

        It wraps the flask-wtf `validate_on_submit`, it needs flask-wtf
        form object to be passed in.
        """
        return form.validate_on_submit()

    def get_site_data(self):
        """Placeholder of site data

        It gets site data from `site_setting` decorator.
        """
        return g.school

    def dispatch_request(self):
        pass
