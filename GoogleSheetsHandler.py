from typing import Optional
import os.path
import googleapiclient.discovery
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


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
        # self._CREDENTIALS_FILE = r"C:\Users\Haskir\creds\google_auth_for_sheet.json"

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(path_to_ini):
            creds = Credentials.from_authorized_user_file(self._CREDENTIALS_FILE, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # try:
        #     service = build('sheets', 'v4', credentials=creds)
        #     sample_range_name = 'Class Data!A2:E'
        #     # Call the Sheets API
        #     sheet = service.spreadsheets()
        #     result = sheet.values().get(spreadsheetId=self._SAMPLE_SPREADSHEET_ID,
        #                                 range=sample_range_name).execute()
        #     values = result.get('values', [])
        #     if not values:
        #         print('No data found.')
        #         return
        #
        #     print('Name, Major:')
        #     for row in values:
        #         # Print columns A and E, which correspond to indices 0 and 4.
        #         print('%s, %s' % (row[0], row[4]))
        # except HttpError as err:
        #     print(err)
        # except BaseException as e:
        #     print(e)


sheetHandler = GoogleSheetsHandler()