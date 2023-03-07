from GoogleDriveHandler import *
from GoogleSheetsHandler import *
from Dataclasses import UserDatabase, User


class UserDbSheetsHandler:
    def __init__(self, g_service: GoogleDriveHandler):
        self.g_service = g_service
        self.db_uid = ""

        if not self.g_service.connected:
            self.g_service.connect()

        for Gfile in self.g_service.show_files():
            if Gfile["name"] == "UserDatabase":
                self.db_uid = Gfile["id"]

        if not self.db_uid:
            self.db_uid = self.g_service.create("UserDatabase")
            print("File UserDatabase has been created in Google Drive")
            self.g_service.create_permission(self.db_uid, "haskird2@gmail.com")

    @classmethod
    def load_db_to_google(cls, UDb: UserDatabase):
        """ НЕ ДОПИСАНО """
        result_list = []
        for user in UDb.database:
            result_list.append(list(user.user_to_dict().values()))

        print(result_list)


if __name__ == "__main__":
    ser = GoogleDriveHandler()
    db = UserDatabase()
    users = [User(1), User(2)]
    for u in users:
        db.add_user(u)
    testHandler = UserDbSheetsHandler(ser)
    testHandler.load_db_to_google(db)

