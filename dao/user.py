from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_user_by_id(self, uid):
        return self.session.query(User).get(uid)

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_data):
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, user_data):
        user = self.get_user_by_id(user_data.get("id"))
        if user_data.get("username"):
            user.username = user_data.get("username")
        if user_data.get("password"):
            user.password = user_data.get("password")
        if user_data.get("role"):
            user.role = user_data.get("role")

        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_user_by_id(uid)
        self.session.delete(user)
        self.session.commit()
