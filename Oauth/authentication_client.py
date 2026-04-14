import os.path
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from gc_agent.dir import BASE_DIR





# If modifying these scopes, delete the file token.json.
#Todo:
    #1.Add scopes for uploading the assigments
SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly",
          "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
          "https://www.googleapis.com/auth/drive.readonly",

          ]

def authenticate():
    PATH = BASE_DIR/"Oauth/token.json"
    creds = None
    if os.path.exists(PATH):
        creds = Credentials.from_authorized_user_file(PATH, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    CREDENTIALS_PATH = Path("gc_agent/Oauth/credentials.json").absolute()
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            
        with open(PATH, "w") as token:
            token.write(creds.to_json())
        return creds
    return creds



if __name__ == "__main__":
  authenticate()