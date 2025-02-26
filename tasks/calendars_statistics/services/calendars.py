from collections.abc import Iterable
from datetime import date
from uuid import UUID

from ..db.repositories import CalendarRepository
from ..models.calendars import Calendar
from ..models.parsing_config import StatisticsParsingConfig


class CalendarService:
    def __init__(
        self,
        calendar_repository: CalendarRepository,
    ) -> None:
        self._calendar = calendar_repository

    async def save_calendar_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        await self._calendar.save_statistics(calendar_id, minutes, date)

    async def get_calendars_to_parse(self, timezones: Iterable[str], filter_date: date) -> list[Calendar]:
        return await self._calendar.get_calendars_to_parse(timezones=timezones, filter_date=filter_date)

    async def get_statistics_parsing_config(self, user_id: UUID) -> StatisticsParsingConfig:
        return await self._calendar.get_statistics_parsing_config(user_id)
