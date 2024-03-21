from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    
    service = build('drive', 'v3', credentials=creds)

    # Calculate the time one week ago
    one_week_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat() + 'Z'

    # Search for files with the name 'samples.txt' modified in the last week
    results = service.files().list(
        q=f"name = 'samples.txt' and modifiedTime > '{one_week_ago}'",
        fields="files(id, name, modifiedTime)").execute()

    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files found:')
        for item in items:
            print(f"{item['name']} (Modified: {item['modifiedTime']})")

if __name__ == '__main__':
    main()


