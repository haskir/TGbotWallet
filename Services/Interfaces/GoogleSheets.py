import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from urllib.error import HTTPError


class GoogleSheets:
    Exist = False

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not GoogleSheets.Exist:
            GoogleSheets.Exist = super().__new__(cls)
            return GoogleSheets.Exist
        return GoogleSheets.Exist

    def __init__(self, path_to_ini: str = "../cred.ini", scopes=None):
        """Shows basic usage of the Sheets API. Print values from a sample spreadsheet"""
        creds = None

        self.service_inner = None
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        with open(path_to_ini, "r") as file:
            self.configs = dict()
            for string in file.readlines():
                self.configs[string.split("=")[0]] = string.split("=")[1].rstrip()
        self._CREDENTIALS_FILE = self.configs.get("account_creds")
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._CREDENTIALS_FILE,
            scopes=scopes)
        httpAuth = credentials.authorize(httplib2.Http())
        self.service_inner = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def show_rows(self, spreadsheet_id: str = None, start: int = 1, stop: int = 1) -> None | list[list]:
        if not start:
            start = 1
        if not stop:
            stop = 1
        response = self.service_inner.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'A{start}:Z{stop}',
            majorDimension="ROWS"
        ).execute()
        if "values" in response:
            return response["values"]
        else:
            return None

    async def edit_row(self, spreadsheet_id: str = None, row: int = 1, data: list[str | int] = []):
        values = {
            "range": f'Sheet1!{row}:{row}',
            "majorDimension": "ROWS",
            "values": [data]
        }
        return self.service_inner.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                                 range=f"Sheet1!{row}:{row}",
                                                                 valueInputOption="USER_ENTERED",
                                                                 body=values,).execute()

    async def append_row(self, spreadsheet_id: str, data: list, category: str = "Sheet1"):
        values = {
            "values": [data]
        }
        self.service_inner.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{category}!A1:I1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=values).execute()

    async def clear_row(self, spreadsheet_id: str, row: int, category: str = "Sheet1!"):
        self.service_inner.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=f"{category}{row}:{row}").execute()

    async def delete_row(self, spreadsheet_id: str, start: int, end: int):
        body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "ROWS",
                            "startIndex": start,
                            "endIndex": end
                        }
                    }
                }
            ]
        }
        self.service_inner.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()

    def last_row(self, spreadsheet_id: str, category: str = "Sheet1!") -> int:
        result = self.service_inner.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{category}A:A").execute()
        if "values" in result.keys():
            return len(result["values"])
        else:
            return 0


# if __name__ == "__main__":
#     from GoogleDriver import GoogleDriver
#
#     service = GoogleDriver()
#     uid = service.create("test")
#     try:
#         sheetHandler = GoogleSheets()
#         await service.create_permission(uid, "haskird2@gmail.com")
#         data_in = [1, 2]
#         sheetHandler.append_row(uid, data_in)
#         sheetHandler.append_row(uid, data_in)
#         # input("Нажми Enter для удаления первой строчки")
#         print(sheetHandler.show(uid))
#         # sheetHandler.clear_row(uid, 1)
#
#         input("Нажми Enter для удаления тестовой таблички")
#     finally:
#         service.delete_tests()
