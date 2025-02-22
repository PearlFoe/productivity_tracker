from pt_bot.calendars.errors import InvalidCalendarIDError
from pt_bot.calendars.models.calendars import Calendar


class GoogleCalendarAPIClientMock:
    def __init__(self, service_account_creds=None, api_name="calendar", api_version="v3") -> None:
        self._db = {}

    async def calendar_info(self, calendar_id: str) -> Calendar:
        if calendar_id not in self._db:
            raise InvalidCalendarIDError(calendar_id=calendar_id)

        return self._db[calendar_id]
