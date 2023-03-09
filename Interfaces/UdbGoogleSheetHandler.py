from Dataclasses import *
from Interfaces import *


class UdbGoogleSheetHandler:
    def __init__(self, googleHandler: GoogleDriver, sheetHandler: GoogleSheets):
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
            self.sheetHandler.append_row(self.db_uid, list(user))

    def upload_db_from_google(self, udb: UserDatabase = UserDatabase()):
        for i in range(self.sheetHandler.last_row(spreadsheet_id=self.db_uid)):
            print()

    def clear_db(self, debug=False):
        for i in range(1, self.sheetHandler.last_row(self.db_uid) + 1):
            self.sheetHandler.clear_row(self.db_uid, i)
            if debug:
                print(f"Clearing row: {i}", end="...\n")


if __name__ == "__main__":
    g_hand = GoogleDriver()
    db = UserDatabase()
    users = [User(i) for i in range(6)]
    s_hand = GoogleSheets()
    for u in users:
        db.add_user(u)
    testHandler = UdbGoogleSheetHandler(g_hand, s_hand)
    testHandler.load_db_to_google(db)
    s_hand.last_row(testHandler.db_uid)
    res = s_hand.get_strings(testHandler.db_uid, 1, 5)
    for item in res:
        print(item)
    input()
    testHandler.clear_db()
