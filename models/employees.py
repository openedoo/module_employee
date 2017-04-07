from .users import User


class Employee(User):

    @staticmethod
    def is_exist(self, username):
        employee = self.query.get(username=username).first()
        return employee

    @classmethod
    def get_public_list(self):
        employees = self.query.with_entities(self.username,
                                             self.fullname,
                                             self.nip)
        return employees
