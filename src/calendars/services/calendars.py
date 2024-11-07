from uuid import UUID

from ..constants.calendar_category import CalendarCategory
from ..db.repositories import CalendarRepository
from .cliens import GoogleCalendarAPIClient


class CalendarService:
    def __init__(
        self,
        calendar_repository: CalendarRepository,
        client: GoogleCalendarAPIClient,
    ) -> None:
        self._calendar = calendar_repository
        self._client = client

    async def add_calendar(self, user_tg_id: int, calendar_id: str) -> UUID:
        calendar = await self._client.calendar_info(calendar_id)
        return await self._calendar.add_calendar(user_tg_id, calendar)

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        await self._calendar.update_calendar_category(calendar_id, calendar_category)
