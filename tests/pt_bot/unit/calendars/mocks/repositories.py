from uuid import UUID, uuid4

from pt_bot.calendars.constants.callback_data import CalendarCategory
from pt_bot.calendars.errors import CalendarDuplicateError
from pt_bot.calendars.models.calendars import Calendar
from pt_bot.calendars.models.schedules import Schedule


class CalendarRepoositoryMock:
    def __init__(self, pool=None, queries=None):
        self._db = {
            "calendars": {},
            "schedules": [],
        }

    def _is_duplicate(self, google_id: str) -> bool:
        return any(c.google_id == google_id for c in self._db["calendars"].values())

    async def add_calendar(self, user_tg_id: int, calendar: Calendar) -> UUID:
        if self._is_duplicate(calendar.google_id):
            raise CalendarDuplicateError(calendar_id=calendar.google_id)

        id_ = uuid4()
        calendar.id = id_
        self._db["calendars"][id_] = calendar
        return id_

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        self._db["calendars"][calendar_id].category = str(calendar_category)

    async def user_has_schedule(self, user_id: UUID) -> bool:
        return any(s.user_id == user_id for s in self._db["schedules"])

    async def add_schedule(self, schedule: Schedule) -> None:
        self._db["schedules"].append(schedule)
