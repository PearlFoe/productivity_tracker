import datetime
import json

from pprint import pp

from google.oauth2 import service_account
from googleapiclient.discovery import build

from settings import Settings
from models.calendars import Calendar
from models.events import Event
from constants import DT_REQUEST_FORMAT


class CalendarParser:
    def __init__(self, service, calendar_id):
        self._service = service
        self._calendar_id = calendar_id
    
    def info(self) -> Calendar:
        data = self._service.calendars().get(calendarId=self._calendar_id).execute()
        return Calendar.model_validate(data)
    
    def events(self, start: datetime, end: datetime) -> list[Event]:
        data = self._service.events().list(
            calendarId=self._calendar_id,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime',
            timeMin=datetime.datetime.strftime(start, DT_REQUEST_FORMAT),
            timeMax=datetime.datetime.strftime(end, DT_REQUEST_FORMAT)
        ).execute()
        return [
            Event.model_validate(event)
            for event in data["items"]
        ]


def main():
    settings = Settings()
    
    account_info = json.loads(settings.google_client_secrets)
    credentials = service_account.Credentials.from_service_account_info(account_info).with_scopes(
        ['https://www.googleapis.com/auth/calendar'],
    )
    
    service = build("calendar", "v3", credentials=credentials)

    parser = CalendarParser(
        service=service,
        calendar_id=settings.calendar_id,
    )
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    pp(parser.events(today, tomorrow))

if __name__ == "__main__":
    main()
