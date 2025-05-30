from uuid import UUID

import asyncpg

from ..constants.callback_data import CalendarCategory
from ..errors import CalendarDuplicateError
from ..models.calendars import Calendar
from ..models.schedules import Schedule
from .queries.builders import CalendarQueryBuilder


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

    async def user_has_schedule(self, user_id: UUID) -> bool:
        async with self._pool.acquire() as connection:
            return await self._queries.user_has_schedule(
                connection=connection,
                user_id=user_id,
            )

    async def add_schedule(self, schedule: Schedule) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.add_schedule(
                connection,
                user_id=schedule.user_id,
                name=schedule.name,
                time=schedule.time,
            )

    async def disable_calendar(self, user_id: UUID, calendar_name: str) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.disable_calendar(
                connection,
                user_id=user_id,
                calendar_name=calendar_name,
            )

    async def get_calendar_names(self, user_id: UUID) -> list[str]:
        async with self._pool.acquire() as connection:
            return await self._queries.get_calendar_names(
                connection,
                user_id=user_id,
            )
