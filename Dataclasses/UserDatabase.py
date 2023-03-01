from User import User


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

    def clear_db(self, *args, psw: int = 1):
        if 5 == psw:
            self.database = []

    def __len__(self):
        return len(self.database)

    def __repr__(self):
        return f"{len(self)}: {self.database}"


