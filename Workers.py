from Services.Interfaces import *


udb = UserDatabase()
googleHandler = GoogleDriver(path_to_ini="./cred.ini")
sheetHandler = GoogleSheets(path_to_ini="./cred.ini")
udb_g_sheet = UdbGoogleSheetHandler(googleHandler=googleHandler, sheetHandler=sheetHandler)
payments_handler = PaymentsGoogleSheet(sheetHandler=sheetHandler)
# for file in googleHandler.show_files():
#     if file["name"] == "UserDatabase":
#         googleHandler.delete_file(file["id"])
udb_g_sheet.load_from_google(udb)

SHEET_UID = "1cbPYocbpmCPqLB-oQByNv1sv9aQHl5lNrjbruRfzF_A"

if __name__ == "__main__":
    users = [User(i) for i in range(7)]
    for u in users:
        udb.add_user(u)
    udb_g_sheet = UdbGoogleSheetHandler(googleHandler, sheetHandler)
    udb_g_sheet.upload_database_to_google(udb)
    sheetHandler.last_row(udb_g_sheet.db_uid)
    input()
    udb_g_sheet.clear_db()
