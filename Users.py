from dataclasses import dataclass


class User:
    def __init__(self, uid: int, name: str):
        self.uid = uid
        self.name = name

    def __repr__(self):
        return f"{self.uid=},{self.name=}"


class UserDatabase:
    Exist = False
    __database = list()

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not UserDatabase.Exist:
            UserDatabase.Exist = super().__new__(cls)
            return UserDatabase.Exist
        return UserDatabase.Exist

    def add_user(self, user_uid: User):
        if isinstance(user_uid, User):
            self.__class__.__database.append(user_uid)
        else:
            raise ValueError

    def __repr__(self):
        return f"{len(self.__class__.__database)}: {self.__class__.__database}"

    def clear_db(self, psw: int = 1):
        if psw == 1:
            self.__class__.__database = []

    def upload_db_to_file(self, file_path: str = "./users_database"):
        from os.path import exists as file_exists

        args = "a" if file_exists(file_path) else "w"
        with open(file_path, args) as file:
            for user in self.__class__.__database:
                file.write(f"{user.uid},{user.name}\n")

    def load_from_file(self, file_path: str = "./users_database"):
        from os.path import exists as file_exists

        if not file_exists(file_path):
            raise FileNotFoundError

        with open(file_path, "r") as file:
            for string in file.readlines():
                uid, name = string.rstrip("\n").split(",")
                self.add_user(User(int(uid), name))


d = UserDatabase()
u1 = User(1, "test1")
u2 = User(2, "test2")
d.add_user(u1)
d.add_user(u2)
print(d)
d.upload_db_to_file()
d.clear_db(1)
print(d)
d.load_from_file()
print(d)