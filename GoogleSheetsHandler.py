from pprint import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsHandler:
    Exist = False

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not GoogleSheetsHandler.Exist:
            GoogleSheetsHandler.Exist = super().__new__(cls)
            return GoogleSheetsHandler.Exist
        return GoogleSheetsHandler.Exist

    def __init__(self, path_to_ini: str = "cred.ini", scopes=None):
        """Shows basic usage of the Sheets API. Print values from a sample spreadsheet"""
        creds = None

        self.service_inner = None
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
        with open(path_to_ini, "r") as file:
            self.configs = dict()
            for string in file.readlines():
                self.configs[string.split("=")[0]] = string.split("=")[1].rstrip()

        self._SAMPLE_SPREADSHEET_ID = self.configs.get("sheet_id")
        self._CREDENTIALS_FILE = self.configs.get("account_creds")
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service_inner = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def show(self, spreadsheet_id: str = None, range: str = "A:1:E10", majorDimension: str = "COLUMNS"):
        # Пример чтения файла
        if not spreadsheet_id:
            spreadsheet_id = self._SAMPLE_SPREADSHEET_ID

        values = self.service_inner.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:E10',
            majorDimension=majorDimension
        ).execute()
        pprint(values)

    def write(self, spreadsheet_id: str):
        # Пример записи в файл
        if not spreadsheet_id:
            spreadsheet_id = self._SAMPLE_SPREADSHEET_ID
        values = self.service_inner.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "B3:C4",
                     "majorDimension": "ROWS",
                     "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
                    {"range": "D5:E6",
                     "majorDimension": "COLUMNS",
                     "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
                ]
            }
        ).execute()


sheetHandler = GoogleSheetsHandler()
sheetHandler.show()
