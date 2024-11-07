from uuid import UUID, uuid4

from bot.calendars.constants.calendar_category import CalendarCategory
from bot.calendars.errors import CalendarDuplicateError
from bot.calendars.models.calendars import Calendar


class CalendarRepoositoryMock:
    def __init__(self, pool=None, queries=None):
        self._db = {}

    def _is_duplicate(self, google_id: str) -> bool:
        return any(c.google_id == google_id for c in self._db.values())

    async def add_calendar(self, user_tg_id: int, calendar: Calendar) -> UUID:
        if self._is_duplicate(calendar.google_id):
            raise CalendarDuplicateError(calendar_id=calendar.google_id)

        id_ = uuid4()
        calendar.id = id_
        self._db[id_] = calendar
        return id_

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        self._db[calendar_id].category = str(calendar_category)
