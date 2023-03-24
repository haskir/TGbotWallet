from Services.Interfaces import *

udb = UserDatabase()
googleHandler = GoogleDriver(path_to_ini="./cred.ini")
sheetHandler = GoogleSheets(path_to_ini="./cred.ini")
udb_g_sheet = UdbGoogleSheetHandler(googleHandler=googleHandler, sheetHandler=sheetHandler)
payments_handler = PaymentsGoogleSheet(sheetHandler=sheetHandler)
# for file in googleHandler.show_files():
#     googleHandler.delete_file(file["id"])
udb_g_sheet.load_from_google(udb)

print("Google files in bot:")
for file in googleHandler.show_files():
    print(f"{file}")

if __name__ == "__main__":
    try:
        user = User({'uid': 1,
                     'is_bot': False,
                     'first_name': 'EMPTY_VALUE',
                     'last_name': 'EMPTY_VALUE',
                     'username': 'EMPTY_VALUE',
                     'language_code': 'EMPTY_VALUE',
                     'email': 'EMPTY_VALUE',
                     'sheet_id': 'EMPTY_VALUE',
                     'permission_id': 0,
                     'state': None})
        input()
    except Exception as e:
        print(e)
    finally:
        googleHandler.delete_tests()
