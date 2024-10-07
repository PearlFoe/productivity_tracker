import datetime
import json

from pprint import pp

from google.oauth2 import service_account
from googleapiclient.discovery import build

from .settings import Settings
from .models.calendars import Calendar
from .models.events import Event



def print_todays_events(service, calendar_id):
    pp(
        service.events().list(
            calendarId=calendar_id,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime',
            timeMin=datetime.datetime.strftime(
                datetime.date.today(),
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            timeMax=datetime.datetime.strftime(
                datetime.date.today() + datetime.timedelta(days=1),
                "%Y-%m-%dT%H:%M:%SZ"
            )
        ).execute()
    )


def print_calendar_info(service, callendar_id):
    pp(
        service.calendars().get(calendarId=callendar_id).execute()
    )


def main():
    settings = Settings()
    
    account_info = json.loads(settings.google_client_secrets)
    credentials = service_account.Credentials.from_service_account_info(account_info).with_scopes(
        ['https://www.googleapis.com/auth/calendar'],
    )
    
    service = build("calendar", "v3", credentials=credentials)

    print_calendar_info(service, settings.calendar_id)


if __name__ == "__main__":
    main()
