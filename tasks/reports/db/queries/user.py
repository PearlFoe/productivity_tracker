from uuid import UUID

import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection


class UserQueryBuilder:
    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    async def load_queries(self, path: str = "sql/", driver: str = "asyncpg") -> None:
        self._queries = aiosql.from_path(path, driver)

    async def get_user_telegram_id(self, connection: Connection, *, user_id: UUID) -> int:
        return await self._queries.get_user_telegram_id(connection, user_id=user_id)

    async def get_users_to_send_report(self, connection: Connection) -> list[UUID]:
        return await self._queries.get_users_to_send_report(connection)
