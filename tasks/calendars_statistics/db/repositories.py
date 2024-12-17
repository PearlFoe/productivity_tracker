from collections.abc import Iterable
from datetime import date
from uuid import UUID

import asyncpg

from ..models.calendars import Calendar
from .queries.builders import CalendarQueryBuilder


class CalendarRepository:
    def __init__(self, pool: asyncpg.Pool, queries: CalendarQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def save_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.save_statistics(
                connection=connection,
                calendar_id=calendar_id,
                minutes=minutes,
                date=date,
            )

    async def get_calendars_by_timezone(self, timezones: Iterable[str]) -> list[Calendar]:
        async with self._pool.acquire() as connection:
            calendars = await self._queries.get_calendars_by_timezone(
                connection=connection,
                timezones=timezones,
            )
            return [Calendar.model_validate(dict(calendar)) for calendar in calendars]
