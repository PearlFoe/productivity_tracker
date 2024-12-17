from collections.abc import Iterable
from datetime import date
from uuid import UUID

import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection


class CalendarQueryBuilder:
    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    async def load_queries(self, path: str = "sql/", driver: str = "asyncpg") -> None:
        self._queries = aiosql.from_path(path, driver)

    async def save_statistics(
        self,
        connection: Connection,
        calendar_id: UUID,
        minutes: int,
        date: date,
    ) -> UUID:
        return await self._queries.save_statistics(
            connection,
            calendar_id=calendar_id,
            minutes=minutes,
            date=date,
        )

    async def get_calendars_by_timezone(self, connection: Connection, timezones: Iterable[str]) -> list[dict]:
        return await self._queries.get_calendars_by_timezone(
            connection,
            timezones=timezones,
        )
