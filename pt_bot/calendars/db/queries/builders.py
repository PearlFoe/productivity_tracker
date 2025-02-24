import datetime
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
        self,
        connection: Connection,
        *,
        tg_id: int,
        google_id: str,
        name: str,
        timezone: str,
        description: str | None = None,
    ) -> UUID:
        return await self._queries.add_calendar(
            connection,
            tg_id=tg_id,
            google_id=google_id,
            name=name,
            description=description,
            timezone=timezone,
        )

    async def update_calendar_category(
        self,
        connection: Connection,
        *,
        calendar_id: UUID,
        category: str,
    ) -> None:
        await self._queries.update_calendar_category(connection, calendar_id=calendar_id, category=category)

    async def user_has_schedule(
        self,
        connection: Connection,
        *,
        user_id: UUID,
    ) -> bool:
        return await self._queries.user_has_schedule(connection, user_id=user_id)

    async def add_schedule(
        self,
        connection: Connection,
        *,
        user_id: UUID,
        name: str,
        time: datetime.time,
    ) -> None:
        await self._queries.add_schedule(
            connection,
            user_id=user_id,
            name=name,
            time=time,
        )

    async def disable_calendar(
        self,
        connection: Connection,
        *,
        user_id: UUID,
        calendar_name: str,
    ) -> None:
        await self._queries.disable_calendar(
            connection,
            user_id=user_id,
            calendar_name=calendar_name,
        )

    async def get_calendar_names(
        self,
        connection: Connection,
        *,
        user_id: UUID,
    ) -> list[str]:
        response = await self._queries.get_calendar_names(connection, user_id=user_id)
        return [record["name"] for record in response]
