# Gmail Imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Other Imports
from datetime import date
import os

class BaseTools():
    def __init__(self):
        self.local_vars = {}

    def getTodaysDate(self):
        return date.today()
    
class GmailTools(BaseTools):
    def __init__(self):
        super().__init__()
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
        self.creds = None

        if os.path.exists("../../secret_client.json"):
            self.creds = Credentials.from_authorized_user_file("../../secret_client.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "../../secret_client.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open("../../secret_client.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            self.service = build("gmail", "v1", credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred: {error}")
    
    def getFolderNames(self) -> list[str]:
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                msg = "API Fetch completed sucessfully. No folders."
                return [], msg
            else:
                msg = f"API Fetch completed sucessfully. There are: {len(labels)} folders found. Deliver it to user and do not make up data."
                return [label['name'] for label in labels], msg

        except HttpError as error:
            print(f"An error occurred: {error}")
            msg = "An error occured while fetching the folder names."
            return [], msg
    
