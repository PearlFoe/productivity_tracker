from datetime import date
from uuid import UUID

import asyncpg

from .queries.builders import CalendarQueryBuilder


class CalendarRepository:
    def __init__(self, pool: asyncpg.Pool, queries: CalendarQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def save_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        async with self._pool.acquire() as connection:
            self._queries.save_statistics(
                connection=connection,
                calendar_id=calendar_id,
                minutes=minutes,
                date=date,
            )
