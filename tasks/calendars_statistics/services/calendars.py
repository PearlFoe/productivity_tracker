from datetime import date
from uuid import UUID

from ..db.repositories import CalendarRepository


class CalendarService:
    def __init__(
        self,
        calendar_repository: CalendarRepository,
    ) -> None:
        self._calendar = calendar_repository

    async def save_calendar_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        self._calendar.save_statistics(calendar_id, minutes, date)
