from .User import User


class UserDatabase:
    Exist = False

    def __init__(self):
        self.database = list()

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not UserDatabase.Exist:
            UserDatabase.Exist = super().__new__(cls)
            return UserDatabase.Exist
        return UserDatabase.Exist

    def add_user(self, user: User) -> bool:
        if isinstance(user, User):
            if user not in self.database:
                self.database.append(user)
                return True
            return False
        else:
            raise ValueError

    def get_user(self, uid: str | int) -> None | User:
        if isinstance(uid, int):
            uid = str(uid)
        for user in self.database:
            if uid == user.uid:
                return user
        return None

    def db_to_list(self) -> list:
        return [user.user_to_dict() for user in self.database]

    def clear_db(self, *args, psw: int = 1):
        if 5 == psw:
            self.database = []

    def __len__(self):
        return len(self.database)

    def __repr__(self):
        return f"{len(self)}: {self.database}"
