from uuid import UUID

import asyncpg

from .queries.builders import CalendarQueryBuilder
from ..models.calendars import Calendar
from ..constants.calendar_category import CalendarCategory
from ..errors import CalendarDuplicateError


class CalendarRepository:
    def __init__(self, pool: asyncpg.Pool, queries: CalendarQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def add_calendar(self, user_tg_id: int, calendar: Calendar) -> UUID:
        async with self._pool.acquire() as connection:
            try:
                return await self._queries.add_calendar(
                    connection=connection,
                    tg_id=user_tg_id,
                    google_id=calendar.google_id,
                    name=calendar.name,
                    timezone=calendar.timezone,
                    description=calendar.description,
                )
            except asyncpg.exceptions.UniqueViolationError as e:
                raise CalendarDuplicateError(calendar_id=calendar.google_id) from e

    async def update_calendar_category(self, calendar_id: UUID, calendar_category: CalendarCategory) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.update_calendar_category(
                connection=connection,
                calendar_id=calendar_id,
                category=calendar_category,
            )
