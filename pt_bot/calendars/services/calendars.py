from uuid import UUID

from ..constants.calendar_category import CalendarCategory
from ..db.repositories import CalendarRepository
from ..models.schedules import DefaultWeeklyReportSchedule
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
        inner_calendar_id = await self._calendar.add_calendar(user_tg_id, calendar)

        # Сделать что-ли middleware для удобного получения user_id по user_tg_id
        # Вроде как можно эту инфу где-то через aiogram сохранять

        schedule = DefaultWeeklyReportSchedule()
        await self._calendar.add_schedule()

        return inner_calendar_id

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        await self._calendar.update_calendar_category(calendar_id, calendar_category)
