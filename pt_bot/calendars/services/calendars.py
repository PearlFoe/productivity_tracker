from uuid import UUID

from pt_bot.core.models.user import User

from ..constants.callback_data import CalendarCategory
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
        if not await self._calendar.user_has_schedule(user_id=user.id):
            await self._calendar.add_schedule(schedule)

        return inner_calendar_id

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        await self._calendar.update_calendar_category(calendar_id, calendar_category)

    async def disable_calendar(self, user: User, calendar_name: str) -> None:
        await self._calendar.disable_calendar(
            user_id=user.id,
            calendar_name=calendar_name,
        )

    async def get_calendar_names(self, user: User) -> list[str]:
        return await self._calendar.get_calendar_names(user.id)
