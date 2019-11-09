'''

'''
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Highest auth scope so that we can create and edit files
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)

def replicate(folderid, destid, driveid):
    results = service.files().list(
       q="'"+folderid+"' in parents",
       fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    parentitem = service.files().get(fileId=folderid)

    parent_metadata = {
            'name': parentitem['name'],
            'driveId': driveid,
            'parents': [destid],
            'mimeType': parentitem['mimeType']
            }

    parentfolder = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
    destid = parentfolder['id']
    
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            file_metadata = {
            'name': item['name'],
            'driveId': driveid,
            'parents': [destid],
            'mimeType': item['mimeType']
            }

            file = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
            print(u'{0} ({1})'.format(item['name'], item['id']))

            if item['mimeType'] == 'application/vnd.google-apps.folder':
                replicate(item['id'], file['id'], driveid)

if __name__ == '__main__':
    folderid = input("enter folderid: ")
    destid = input("destid: ")
    driveid = input("driveid: ")

    replicate(folderid, destid, driveid)