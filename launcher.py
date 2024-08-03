import datetime
import os.path
import re
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/calendar"]

team = os.getenv('TEAM')

def get_macthes():
    with open('matches.txt', 'r') as file:
        data = file.read()

    # Regex to transform file data
    pattern = r'(.+?) vs (.+?), Date: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})'
    matches = re.findall(pattern, data)

    return matches


def create_events(service, matches):
    for match in matches:
        final_time = timedelta(hours = 2)
        is_local = True if match[0] == team else False
        
        date = match[2]
        hour = match[3]
        date_time_str = f"{date} {hour}"
        date_time_start = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        event = {
            "summary": f'{match[0]} vs {match[1]}',
            "colorId": '2' if is_local else '4', #Green if its local, Orange if its visitor
            "start": {
                "dateTime": date_time_start.isoformat(),
                "timeZone": 'Europe/Madrid'
            },
            "end": {
                "dateTime": (date_time_start + final_time).isoformat(),
                "timeZone": 'Europe/Madrid'
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
    

    
def authenticate_google():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    service = build("calendar", "v3", credentials=creds)
    return service



def main():
    service = authenticate_google()
    create_events(service, get_macthes())

    # Call the Calendar API



if __name__ == "__main__":
    main()