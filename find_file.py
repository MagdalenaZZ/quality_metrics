from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import os
import subprocess

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Folder ID for 'https://drive.google.com/drive/folders/1otnVON0SGVUHveQg4huhFx4TF_Xi1yym'
    folder_id = '1otnVON0SGVUHveQg4huhFx4TF_Xi1yym'
    query = f"'{folder_id}' in parents and name = 'samples.txt'"

    # Search for the samples.txt file in the specified folder
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            print(f"Found file: {item['name']} (ID: {item['id']})")
            download_file_from_google_drive(item['id'], item['name'])
            
            # Here are instructions to run the file parser

            # Define the command you want to run as a list
            command = ['python', 'parse_and_email.py', 'samples.txt']

            # Run the command
            process = subprocess.run(command, capture_output=True, text=True)

            # Check if the command was successful
            if process.returncode == 0:
                print("Command executed successfully.")
                # If you want to print the output
                print("Output:", process.stdout)
            else:
                print("Command failed.")
                # If you want to print the error
                print("Error:", process.stderr)

def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print(f"Downloaded '{destination}'")

if __name__ == '__main__':
    main()




