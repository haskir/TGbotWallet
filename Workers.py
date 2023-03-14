from Services.Interfaces import *


udb = UserDatabase()
googleHandler = GoogleDriver(path_to_ini="./cred.ini")
sheetHandler = GoogleSheets(path_to_ini="./cred.ini")
udb_g_sheet = UdbGoogleSheetHandler(googleHandler=googleHandler, sheetHandler=sheetHandler)
payments_handler = PaymentsGoogleSheet(sheetHandler=sheetHandler)
googleHandler.delete_tests()

SHEET_UID = "1cbPYocbpmCPqLB-oQByNv1sv9aQHl5lNrjbruRfzF_A"


if __name__ == "__main__":
    user = User(1)
    user.state = {"Category": "Еда",
                  "Market": "Пятёрочка",
                  "Total": "100",
                  "Description": "Хлебушек"}
    # try:
    payments_handler = PaymentsGoogleSheet(sheetHandler)
    payments_handler.delete_payment(SHEET_UID, 6)
    # except Exception as e:
    #     print(e)
