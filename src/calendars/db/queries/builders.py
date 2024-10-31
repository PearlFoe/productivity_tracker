from uuid import UUID

import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection


class CalendarQueryBuilder:
    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    async def load_queries(self, path: str = "sql/", driver: str = "asyncpg") -> None:
        self._queries = aiosql.from_path(path, driver)

    async def add_calendar(
        self, connection: Connection, tg_id: int, name: str, timezone: str, description: str = None
    ) -> UUID:
        id_ = await self._queries.add_calendar(
            connection,
            tg_id=tg_id,
            name=name,
            description=description,
            timezone=timezone,
        )
        return UUID(id_)

    async def update_calendar_category(
        self, connection: Connection, calendar_id: UUID, category: str
    ) -> None:
        await self._queries.update_calendar_category(connection, calendar_id=calendar_id, category=category)
