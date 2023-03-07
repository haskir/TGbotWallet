from GoogleDriveHandler import *
from GoogleSheetsHandler import *
from Dataclasses import UserDatabase, User


class UserDbSheetsHandler:
    def __init__(self, googleHandler: GoogleDriveHandler, sheetHandler: GoogleSheetsHandler):
        self.googleHandler = googleHandler
        self.sheetHandler = sheetHandler
        self.db_uid = ""

        for Gfile in self.googleHandler.show_files():
            if Gfile["name"] == "UserDatabase":
                self.db_uid = Gfile["id"]

        if not self.db_uid:
            self.db_uid = self.googleHandler.create("UserDatabase")
            print("File UserDatabase has been created in Google Drive")
            self.googleHandler.create_permission(self.db_uid, "haskird2@gmail.com")

    def load_db_to_google(self, UDb: UserDatabase):
        for user in UDb.database:
            print(user)
            self.sheetHandler.append_row(self.db_uid, user.user_to_list())

    def clear_db(self, debug=False):
        for i in range(1, self.sheetHandler.last_row(self.db_uid)+1):
            self.sheetHandler.clear_row(self.db_uid, i)
            if debug:
                print(f"Clearing row: {i}", end="...\n")


if __name__ == "__main__":
    g_hand = GoogleDriveHandler()
    db = UserDatabase()
    users = [User(i) for i in range(6)]
    s_hand = GoogleSheetsHandler()
    for u in users:
        db.add_user(u)
    testHandler = UserDbSheetsHandler(g_hand, s_hand)
    testHandler.load_db_to_google(db)
    s_hand.last_row(testHandler.db_uid)
    input()
    testHandler.clear_db()
