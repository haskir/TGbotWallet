from typing import Optional
import os.path
import googleapiclient.discovery
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleHandler:
    Exist = False

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not GoogleHandler.Exist:
            GoogleHandler.Exist = super().__new__(cls)
            return GoogleHandler.Exist
        return GoogleHandler.Exist

    def __init__(self, path_to_ini: str = "cred.ini", scopes=None):
        self.service_inner = None
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/spreadsheets',
                      'https://www.googleapis.com/auth/drive']
        with open(path_to_ini, "r") as file:
            self.configs = dict()
            for string in file.readlines():
                self.configs[string.split("=")[0]] = string.split("=")[1].rstrip()

        self._SAMPLE_SPREADSHEET_ID = self.configs.get("sheet_id")
        self._CREDENTIALS_FILE = self.configs.get("account_creds")

    def connect(self, output: bool = False) -> googleapiclient.discovery.build:
        """If output == True prints array of files"""
        creds, _ = google.auth.load_credentials_from_file(self._CREDENTIALS_FILE)
        self.service_inner = build(serviceName='drive', version='v3', credentials=creds)
        files = []

        if output:
            print(self.show_files())

    def show_files(self) -> list:
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = self.service_inner.files().list(
                fields='nextPageToken, files(id, name)',
                pageToken=page_token).execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    def create_folder(self, names_for_folders: str) -> bool:
        try:
            file_metadata = {
                'name': names_for_folders,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            self.service_inner.files().create(body=file_metadata, fields='id').execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True

    def delete_file(self, name_for_file: str) -> bool:
        try:
            self.service_inner.files().delete(fileId=name_for_file).execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True


if __name__ == '__main__':
    service = GoogleHandler()
    service.connect()
    # service.create_folder("Test_Folder")
    service.delete_file(service.show_files()[0]["id"])
    print(service.show_files())