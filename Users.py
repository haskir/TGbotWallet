from dataclasses import dataclass
from TXTFileDB import TxtFileWorker


@dataclass
class User:
    uid: int = 0
    is_bot: bool = False
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    language_code: str = ""

    def __repr__(self):
        return f"{self.uid};{self.is_bot};{self.first_name};{self.last_name};{self.username};{self.language_code}"


class UserDatabase:
    Exist = False

    def __init__(self):
        self.__database = list()

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not UserDatabase.Exist:
            UserDatabase.Exist = super().__new__(cls)
            return UserDatabase.Exist
        return UserDatabase.Exist

    def add_user(self, UserData: User | list):
        if isinstance(UserData, User):
            self.__database.append(UserData)
        elif isinstance(UserData, list):
            for string in UserData:
                uid, name = string.strip("\n").split(",")
                self.add_user(User(uid, name))
        else:
            raise ValueError

    def clear_db(self, psw: int = 2):
        if 1 == psw:
            self.__database = []

    @property
    def database(self):
        return self.__database

    def __repr__(self):
        return f"{len(self.__database)}: {self.__database}"


u1 = User(1)
u2 = User(2)
d = UserDatabase()
