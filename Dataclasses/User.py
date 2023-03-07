class User:
    def __init__(self, uid: int = 0,
                 is_bot: bool = False,
                 first_name: str = "",
                 last_name: str = "",
                 username: str = "",
                 language_code: str = "",
                 email: str = "",
                 sheet_id: str = "",
                 permission_id: int = 0
):
        self.uid = uid
        self.is_bot = is_bot
        self.first_name = first_name or "EMPTY_VALUE"
        self.last_name = last_name or "EMPTY_VALUE"
        self.username = username or "EMPTY_VALUE"
        self.language_code = language_code or "EMPTY_VALUE"
        self.email = email or "EMPTY_VALUE"
        self.sheet_id = sheet_id or "EMPTY_VALUE"
        self.permission_id = permission_id

    def __eq__(self, other):
        if isinstance(other, User):
            return self.uid == other.uid
        else:
            return False

    @classmethod
    def create_user_from_dict(cls, pairs: dict):
        return User(*[value for value in pairs.values()])

    def user_to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items()}

    def user_to_list(self) -> list:
        return list(self.__dict__.values())

    def __repr__(self):
        return f"User : {str({key: value for key, value in self.__dict__.items()})}\n"


if __name__ == "__main__":
    u1 = User(1)
    print(u1.user_to_list())