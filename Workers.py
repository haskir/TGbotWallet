from Services.Interfaces import *

udb = UserDatabase()
googleHandler = GoogleDriver(path_to_ini="./cred.ini")
sheetHandler = GoogleSheets(path_to_ini="./cred.ini")
udb_g_sheet = UdbGoogleSheetHandler(googleHandler=googleHandler, sheetHandler=sheetHandler)
payments_handler = PaymentsGoogleSheet(sheetHandler=sheetHandler)


def __print_google_files():
    print("Google files in bot:")
    for file in googleHandler.show_files():
        if file["name"] == "EMPTY_VALUE":
            googleHandler.delete_file(file["id"])
        print(f"{file}")


if udb_g_sheet.load_from_google(udb):
    print("Connected to Google!")


if __name__ == "__main__":
    __print_google_files()
