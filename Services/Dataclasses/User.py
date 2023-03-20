from aiogram.filters.state import State


class User:
    ATTRS = ["uid",
             "inner_name",
             "first_name",
             "last_name",
             "username",
             "language_code",
             "email",
             "sheet_id",
             "permission_id",
             "state"]

    def __init__(self, uid: str | int | list | dict,
                 inner_name: str = "",
                 first_name: str = "",
                 last_name: str = "",
                 username: str = "",
                 language_code: str = "",
                 email: str = "",
                 sheet_id: str = "",
                 permission_id: str = "",
                 state: str = ""):
        """ Accepts *args or list or dict"""
        if isinstance(uid, int | str):
            self.uid = str(uid) or 1
            self.inner_name = inner_name or "EMPTY_VALUE"
            self.first_name = first_name or "EMPTY_VALUE"
            self.last_name = last_name or "EMPTY_VALUE"
            self.username = username or "EMPTY_VALUE"
            self.language_code = language_code or "EMPTY_VALUE"
            self.email = email or "EMPTY_VALUE"
            self.sheet_id = sheet_id or "EMPTY_VALUE"
            self.permission_id = permission_id or "EMPTY_VALUE"
            self.state = {}
        elif (isinstance(uid, list) and len(User.ATTRS) != len(uid)) or \
                (isinstance(uid, dict) and len(User.ATTRS) != len(uid.keys())):
            raise ValueError(f"Not expected length in initialization, expected {len(User.ATTRS)}, got {len(uid)}")
        elif isinstance(uid, dict):
            self.__dict__ = {key: value for key, value in uid.items()}
        elif isinstance(uid, list):
            self.__dict__ = {User.ATTRS[key]: value for key, value in enumerate(uid)}
        else:
            raise ValueError("Not expected type in initialization")

    @classmethod
    def __call__(cls, pairs: dict):
        return User(pairs)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.uid == other.uid
        else:
            return False

    def __iter__(self):
        return iter([value for key, value in self.__dict__.items() if key != "state"])

    def __next__(self):
        return next(iter(self))

    def __repr__(self):
        return f"User : {str({key: value for key, value in self.__dict__.items() if key != 'state'})}\n"


if __name__ == "__main__":
    u1 = User(1)
    test_1 = User(1)
    test_l = User([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, []])
    test_d = {'uid': 1, 'is_bot': False, 'first_name': 'EMPTY_VALUE', 'last_name': 'EMPTY_VALUE',
              'username': 'EMPTY_VALUE', 'language_code': 'EMPTY_VALUE', 'email': 'EMPTY_VALUE',
              'sheet_id': 'EMPTY_VALUE', 'permission_id': 0, 'state': None, 'categories': []}
    print(test_1)
    print(test_l)
    print(User(test_d))
    print(dict(test_l))
