from ..models.user_model import UserModel


class UserService:
    def __init__(self):
        self.user_model = UserModel()

    def add(self, id, first_name, last_name, username):
        return self.user_model.create(id, first_name, last_name, username)

    def remove(self, id):
        return self.user_model.delete(id)

    def exist(self, id):
        return self.user_model.exist(id)
