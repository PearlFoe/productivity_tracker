import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection


class UserQuery:
    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    async def load_queries(self, path: str = "sql/", driver: str = "asyncpg") -> None:
        self._queries = aiosql.from_path(path, driver)

    async def get_user(self, connection: Connection, tg_id: int) -> int | None:
        return await self._queries.get_user(connection, tg_id=tg_id)

    async def create_user(self, connection: Connection, tg_id: int) -> None:
        await self._queries.create_user(connection, tg_id=tg_id)
