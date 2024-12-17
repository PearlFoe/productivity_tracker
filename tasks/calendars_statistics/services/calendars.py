from collections.abc import Iterable
from datetime import date
from uuid import UUID

from ..db.repositories import CalendarRepository
from ..models.calendars import Calendar


class CalendarService:
    def __init__(
        self,
        calendar_repository: CalendarRepository,
    ) -> None:
        self._calendar = calendar_repository

    async def save_calendar_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        await self._calendar.save_statistics(calendar_id, minutes, date)

    async def get_calendars_by_timezone(self, timezones: Iterable[str]) -> list[Calendar]:
        return await self._calendar.get_calendars_by_timezone(timezones=timezones)
