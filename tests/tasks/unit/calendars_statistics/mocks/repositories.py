from collections.abc import Iterable
from datetime import date
from uuid import UUID

from tasks.calendars_statistics.models.calendars import Calendar
from tasks.calendars_statistics.models.parsing_config import StatisticsParsingConfig


class CalendarRepository:
    def __init__(self, pool=None, queries=None):
        self._db = {
            "statistics": {},
            "calendars": {},
            "parsing_config": {},
        }

    async def save_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        self._db["statistics"][calendar_id] = {
            "minutes": minutes,
            "date": date,
        }

    async def get_calendars_to_parse(self, timezones: Iterable[str], filter_date: date) -> list[Calendar]:
        return [calendar for calendar in self._db["calendars"].values() if calendar.timezone in timezones]

    async def get_statistics_parsing_config(self, user_id: UUID) -> StatisticsParsingConfig:
        return self._db["parsing_config"][user_id]
