import pprint
from openedoo.core.libs import blueprint
from openedoo.core.db import Query

module_employee = blueprint('employee', __name__)


@module_employee.route('/', methods=['POST', 'GET'])
def index():
    return 'ko'
