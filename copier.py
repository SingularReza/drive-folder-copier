import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def replicate(folderid, destid):
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
       q="folderid in parents", fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    for folder in items:
        file_metadata = {
            'name': folder.name,
            'parents': destid,
            'mimeType': folder.mimeType
        }

        file = drive_service.files().create(body=file_metadata, fields='id').execute()

        if mimeType == 'application/vnd.google-apps.folder':
            replicate(folder.id, file.id)

if __name__ == '__main__':
    folderid = input("enter folderid: ")
    destid = input("destid: ")

    replicate(folderid, destid)
