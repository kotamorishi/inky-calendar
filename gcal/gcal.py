import time
import os.path
from datetime import datetime
from sys import maxsize
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from events import Events

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Google_Calendar:
    def __init__(self, startDate, endDate):
        self.events = []
        # convert date to datetime.
        self.startDate = datetime.combine(startDate, datetime.min.time())
        self.endDate = datetime.combine(endDate, datetime.max.time())
        self.updated_at = datetime.now()
        self.get_calendar()

    def get_calendar(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0) # local server storategy(too Mendokusai to update here..)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        #Load range of the google calendar based on startDate to endDate.
        #print("Google Calendar load range " + self.startDate.isoformat() + " to " + self.endDate.isoformat())

        # Call the Calendar API
        # time format should be like 2021-11-23T03:03:33.804Z
        events_result = service.events().list(
            calendarId='primary',
            timeMin=self.startDate.isoformat() + 'Z',
            maxResults=250,
            singleEvents=True,
            timeMax=self.endDate.isoformat() + 'Z',
            orderBy='startTime').execute()

        gcal_events = events_result.get('items', [])
        self.updated_at = events_result.get('updated') # latest update datetime store into "updated_at"

        # order events into dates
        events = Events(self.startDate, self.endDate)
        for event in gcal_events:
            raw_start = event['start'].get('dateTime', event['start'].get('date'))
            if validate_long_dt(raw_start):
                start_dt = datetime.strptime(raw_start, '%Y-%m-%dT%H:%M:%S%z')
            elif validate_short_dt(raw_start):
                start_dt = datetime.strptime(raw_start, '%Y-%m-%d')

            raw_end = event['end'].get('dateTime', event['end'].get('date'))
            if validate_long_dt(raw_end):    
                end_dt = datetime.strptime(raw_end, '%Y-%m-%dT%H:%M:%S%z')
            elif validate_short_dt(raw_end):
                end_dt = datetime.strptime(raw_end, '%Y-%m-%d')
            
            if start_dt and end_dt:
                summary=event['summary']
                description = ""
                if 'description' in event:
                    description=event['description']
                events.add_event(start=start_dt, end=end_dt, title=summary, description=description)

        self.events = events

def validate_long_dt(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z')
        return True
    except ValueError:
        return False

def validate_short_dt(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

