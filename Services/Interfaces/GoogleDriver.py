import googleapiclient.discovery
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDriver:
    Exist = False

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not GoogleDriver.Exist:
            GoogleDriver.Exist = super().__new__(cls)
            return GoogleDriver.Exist
        return GoogleDriver.Exist

    def __init__(self, path_to_ini: str = "../cred.ini", scopes=None):
        self.service_inner = None
        self.connected: bool = False
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/drive,'
                      'https://www.googleapis.com/auth/drive.file',
                      'https://www.googleapis.com/auth/spreadsheets']
        with open(path_to_ini, "r") as file:
            self.configs = dict()
            for string in file.readlines():
                self.configs[string.split("=")[0]] = string.split("=")[1].rstrip()
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

    async def create(self, name: str, is_folder: bool = False) -> str | None:
        if not self.connected:
            self.__connect()
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder' if is_folder else 'application/vnd.google-apps.spreadsheet'
        }
        try:
            result = await self.service_inner.files().create(body=file_metadata, fields='id').execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return None
        return result["id"]

    async def delete_file(self, file_id: str) -> bool:
        if not self.connected:
            self.__connect()
        try:
            self.service_inner.files().delete(fileId=file_id).execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True

    async def create_permission(self, file_id: str, user_email: str, role: str = "reader") -> int:
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
            result = await self.service_inner.permissions().create(fileId=file_id,
                                                                   body=user_permission).execute()
        except HttpError as error:
            response = f"Error while getting permissions {error}"
            print(response)
            return False
        return result["id"]

    async def delete_tests(self):
        if not self.connected:
            self.__connect()
        for file in await self.show_files():
            if "test" == file["name"]:
                await self.delete_file(file["id"])

    async def download_sheet(self, file_od: str):
        from googleapiclient.http import MediaIoBaseDownload
        import io
        try:
            # create drive api client
            file_id = file_od
            # pylint: disable=maybe-no-member
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            request = self.service_inner.files().export_media(fileId=file_id,
                                                              mimeType=mime)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = await downloader.next_chunk()

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.getvalue()


if __name__ == '__main__':
    service = GoogleDriver()
    my_file_id = "1dqTL3Q31stG5R09Nv3iL6_UW9g0z9FjuCszvQbn1JPQ"
    service.download_sheet(my_file_id)
