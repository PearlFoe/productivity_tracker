from collections.abc import Iterable
from datetime import date
from uuid import UUID

from tasks.calendars_statistics.models.calendars import Calendar


class CalendarRepository:
    def __init__(self, pool=None, queries=None):
        self._db = {
            "statistics": {},
            "calendars": {},
        }

    async def save_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        self._db["statistics"][calendar_id] = {
            "minutes": minutes,
            "date": date,
        }

    async def get_calendars_by_timezone(self, timezones: Iterable[str]) -> list[Calendar]:
        return [calendar for calendar in self._db["calendars"].values() if calendar.timezone in timezones]