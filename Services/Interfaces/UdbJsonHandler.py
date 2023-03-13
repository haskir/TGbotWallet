from json import load, dump
from Services.Dataclasses import *


class UDbJsonHandler:
    default = r"../TempFiles/users_database.json"

    def __init__(self, userdatabase: UserDatabase = UserDatabase()):
        self.userdatabase = userdatabase

    def upload_db_to_file(self, file_path: str = default) -> None:
        from os.path import exists as file_exists

        args = "a" if file_exists(file_path) else "w"

        with open(file_path, args) as file:
            dump([user.user_to_dict() for user in self.userdatabase.database], file)

    def load_db_from_file(self, file_path: str = default) -> bool | None:
        from os.path import exists as file_exists

        if not file_exists(file_path):
            raise FileNotFoundError

        with open(file_path, "r") as file:
            for user in load(file):
                self.userdatabase.add_user(User(user))
            return True

    def __repr__(self):
        return self.userdatabase.__repr__()

    @classmethod
    def clear_json_file(cls, file_path: str = default):
        from os.path import exists as file_exists

        if not file_exists(file_path):
            raise FileNotFoundError

        with open(file_path, "w") as file:
            return True


if __name__ == '__main__':
    users = [User(1), User(2), User(1)]
    db = UserDatabase()
    for user in users:
        db.add_user(user)
    print(db)
    print("\n\n\n")
    jh = UDbJsonHandler(db)
    jh.upload_db_to_file()
    db.clear_db(psw=5)
    jh.load_db_from_file()
    jh.clear_json_file()
    print(jh)