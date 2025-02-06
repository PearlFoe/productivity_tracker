from datetime import date
from uuid import UUID

import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection


class ReportQueryBuilder:
    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    async def load_queries(self, path: str = "sql/", driver: str = "asyncpg") -> None:
        self._queries = aiosql.from_path(path, driver)

    async def get_user_calendars(
        self,
        connection: Connection,
        *,
        user_id: UUID,
    ) -> list[tuple[UUID, str]]:
        return await self._queries.get_user_calendars(
            connection,
            user_id=user_id,
        )

    async def get_calendar_statistics(
        self,
        connection: Connection,
        *,
        calendar_id: UUID,
        start: date,
        end: date,
    ) -> list[dict]:
        return await self._queries.get_calendar_statistics(
            connection,
            calendar_id=calendar_id,
            start=start,
            end=end,
        )
