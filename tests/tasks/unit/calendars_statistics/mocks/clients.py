from datetime import datetime

from tasks.calendars_statistics.models.client.events import Event


class GoogleCalendarAPIClientMock:
    def __init__(self, service_account_creds=None, api_name="calendar", api_version="v3") -> None:
        self._db = {}

    async def events(self, calendar_id: str, start: datetime, end: datetime) -> list[Event]:
        return self._db[calendar_id]
