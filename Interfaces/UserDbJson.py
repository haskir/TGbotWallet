from json import load, dump
from Dataclasses import User, UserDatabase


class UserDbJson:
    default = r"../TempFiles/users_database.json"

    def __init__(self, userdatabase: UserDatabase):
        self.userdatabase = userdatabase

    def upload_db_to_file(self, file_path: str = default) -> None:
        from os.path import exists as file_exists

        args = "a" if file_exists(file_path) else "w"

        with open(file_path, args) as file:
            dump([user.user_to_dict() for user in self.userdatabase.database], file)

    def load_db_from_file(self, file_path: str = default) -> list:
        from os.path import exists as file_exists

        if not file_exists(file_path):
            raise FileNotFoundError

        with open(file_path, "r") as file:
            for user in load(file):
                temp_u = User


print(__import__())
