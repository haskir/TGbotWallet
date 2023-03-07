from typing import Optional
import os.path
import googleapiclient.discovery
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleDriveHandler:
    Exist = False

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not GoogleDriveHandler.Exist:
            GoogleDriveHandler.Exist = super().__new__(cls)
            return GoogleDriveHandler.Exist
        return GoogleDriveHandler.Exist

    def __init__(self, path_to_ini: str = "../cred.ini", scopes=None):
        self.service_inner = None
        self.connected: bool = False
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/drive,'
                      'https://www.googleapis.com/auth/drive.file']
        with open(path_to_ini, "r") as file:
            self.configs = dict()
            for string in file.readlines():
                self.configs[string.split("=")[0]] = string.split("=")[1].rstrip()

        self._SAMPLE_SPREADSHEET_ID = self.configs.get("sheet_id")
        self._CREDENTIALS_FILE = self.configs.get("account_creds")

    def __connect(self, output: bool = False) -> googleapiclient.discovery.build:
        """If output == True prints array of files"""
        creds, _ = google.auth.load_credentials_from_file(self._CREDENTIALS_FILE)
        self.service_inner = build(serviceName='drive', version='v3', credentials=creds)
        files = []
        self.connected = True
        if output:
            print(self.show_files())

    def show_files(self) -> list | bool:
        if not self.connected:
            self.__connect()
        files = []
        page_token = None
        try:
            while True:
                # pylint: disable=maybe-no-member
                response = self.service_inner.files().list(
                    fields='nextPageToken, files(id, name)',
                    pageToken=page_token).execute()
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        else:
            return files

    def create(self, name: str, is_folder: bool = False) -> str:
        if not self.connected:
            self.__connect()
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder' if is_folder else 'application/vnd.google-apps.spreadsheet'
        }
        try:
            result = self.service_inner.files().create(body=file_metadata, fields='id').execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return result["id"]

    def delete_file(self, file_id: str) -> bool:
        if not self.connected:
            self.__connect()
        try:
            self.service_inner.files().delete(fileId=file_id).execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True

    def create_permission(self, file_id: str, user_email: str, role: str = "reader") -> int:
        if not self.connected:
            self.__connect()
        """ possible role == organizer writer reader
            returns permission id """
        user_permission = {
            'role': role,
            'type': "user",
            'emailAddress': user_email,
        }
        try:
            result = self.service_inner.permissions().create(fileId=file_id,
                                                             body=user_permission).execute()
        except HttpError as error:
            response = f"Error while getting permissions {error}"
            print(response)
            return False
        return result["id"]

    def delete_tests(self):
        if not self.connected:
            self.__connect()
        for file in self.show_files():
            if "test" == file["name"]:
                self.delete_file(file["id"])


if __name__ == '__main__':
    service = GoogleDriveHandler()
    for file in service.show_files():
        if "test" == file["name"]:
            service.delete_file(file["id"])
    test_file_id = service.create("test")
    print(service.show_files())
    print(service.create_permission(test_file_id, "haskird2@gmail.com"))
    input("\n\n")
    service.delete_file(test_file_id)
    print(service.show_files())
