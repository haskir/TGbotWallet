from Services.Interfaces import *
import dotenv
import os
from aiogram import Bot

dotenv.load_dotenv()
TGbotWallet_token: str = os.getenv('TGbotWallet_token')
bot: Bot = Bot(token=TGbotWallet_token)
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
    my_file_id = "1dqTL3Q31stG5R09Nv3iL6_UW9g0z9FjuCszvQbn1JPQ"
    file_d = googleHandler.download_sheet(my_file_id)
    if file_d:
        with open("test_download.xlsx", "wb") as file:
            file.write(file_d)