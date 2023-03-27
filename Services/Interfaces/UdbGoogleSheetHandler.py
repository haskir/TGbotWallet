from Services.Interfaces import *


class UdbGoogleSheetHandler:
    def __init__(self, googleHandler: GoogleDriver, sheetHandler: GoogleSheets):
        self.googleHandler = googleHandler
        self.sheetHandler = sheetHandler
        self.db_uid = ""

        for Gfile in self.googleHandler.show_files():
            if Gfile["name"] == "UserDatabase":
                self.db_uid = Gfile["id"]
                print(f"UserDatabase uid:\n{self.db_uid}")

        if not self.db_uid:
            self.db_uid = self.googleHandler.create("UserDatabase")
            print("File UserDatabase has been created in Google Drive")
            self.googleHandler.create_permission(self.db_uid, "haskird2@gmail.com", role="writer")

    async def upload_database_to_google(self, user_database: UserDatabase):
        last = await self.sheetHandler.last_row(spreadsheet_id=self.db_uid)
        if last:
            rows = await self.sheetHandler.show_rows(spreadsheet_id=self.db_uid, start=1, stop=last)
            print("{rows=}")
            uids_on_google = [row[0] for row in rows]
            print(f"{uids_on_google=}")
            for user in user_database:
                if user.uid not in uids_on_google:
                    await self.__upload_new_user_to_google(user)
        else:
            for user in user_database:
                self.__upload_new_user_to_google(user)

    def __upload_new_user_to_google(self, user: User):
        self.sheetHandler.append_row(spreadsheet_id=self.db_uid,
                                     data=list(user))

    async def user_already_in_google_db(self, user: User | str) -> bool:
        last = await self.sheetHandler.last_row(spreadsheet_id=self.db_uid)
        if not last:
            return False
        user_uid = user.uid if isinstance(user, User) else user
        return user_uid in [row[0] for row in self.sheetHandler.show_rows(spreadsheet_id=self.db_uid,
                                                                          start=1,
                                                                          stop=last)]

    async def update_user(self, user: User):
        last = await self.sheetHandler.last_row(spreadsheet_id=self.db_uid)
        if not last:
            last = 1
            await self.sheetHandler.append_row(spreadsheet_id=self.db_uid,
                                               data=list(user))
        else:
            for key, row in enumerate(await self.sheetHandler.show_rows(spreadsheet_id=self.db_uid,
                                                                        start=0, stop=last)):
                if row[0] == user.uid:
                    await self.sheetHandler.edit_row(spreadsheet_id=self.db_uid,
                                                     row=key + 1,
                                                     data=list(user))
                    return True
            await self.sheetHandler.append_row(spreadsheet_id=self.db_uid,
                                               data=list(user))

    def load_from_google(self, user_database: UserDatabase) -> bool:
        last = self.sheetHandler.last_row(spreadsheet_id=self.db_uid)
        if last:
            users = self.sheetHandler.show_rows(spreadsheet_id=self.db_uid,
                                                start=1, stop=last)
            [user_database.add_user(User(*user)) for user in users]
            return True
        else:
            return False

    async def clear_db(self, debug=False):
        for i in range(1, await self.sheetHandler.last_row(self.db_uid) + 1):
            await self.sheetHandler.clear_row(self.db_uid, i)
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
    testHandler.upload_database_to_google(db)
    s_hand.last_row(testHandler.db_uid)
    res = s_hand.show_rows(testHandler.db_uid, 1, 5)
    for item in res:
        print(item)
    input()
    testHandler.clear_db()
