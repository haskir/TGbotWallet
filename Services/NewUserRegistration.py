from Interfaces.GoogleDriveHandler import GoogleDriveHandler
from Dataclasses.User import User


def create_sheet_for_new_user(user: User) -> str:
    drive_handler = GoogleDriveHandler()
    drive_handler.connect()
    user.sheet_id = drive_handler.create(str(user.uid))
    return user.sheet_id
