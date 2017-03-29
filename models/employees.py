from .users import User


class Employee(User):

    @staticmethod
    def is_exist(self, username):
        employee = self.query.get(username=username).first()
        return employee
