from uuid import UUID

from pt_bot.core.models.user import User

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

    async def add_calendar(self, user: User, calendar_id: str) -> UUID:
        calendar = await self._client.calendar_info(calendar_id)
        inner_calendar_id = await self._calendar.add_calendar(user.telegram_id, calendar)

        schedule = DefaultWeeklyReportSchedule(user_id=user.id)
        await self._calendar.add_schedule(schedule)

        return inner_calendar_id

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        await self._calendar.update_calendar_category(calendar_id, calendar_category)
