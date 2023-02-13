from __future__ import print_function
import os.path
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']


def main():
    with open("cred.ini", "r") as file:
        configs = {}
        for string in file.readlines():
            configs[string.split("=")[0]] = string.split("=")[1].rstrip()
        # print(f"{configs=}")

    SAMPLE_SPREADSHEET_ID = configs.get("sheet_id")
    CREDENTIALS_FILE = configs.get("account_creds")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    httpauth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("sheets", "v4", http=httpauth)

    values = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="A1:E10",
        majorDimension="ROWS"
    ).execute()
    print(values)

    # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     print(1)
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #         print(2)
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())
    #
    # try:
    #     service = build('sheets', 'v4', credentials=creds)
    #
    #     # Call the Sheets API
    #     sheet = service.spreadsheets()
    #     result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                                 range=SAMPLE_RANGE_NAME).execute()
    #     values = result.get('values', [])
    #
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


if __name__ == '__main__':
    main()
