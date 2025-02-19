import aiosql
from aiosql.queries import Queries as AiosqlQueries
from asyncpg import Connection


class UserQueryBuilder:
    def __init__(self) -> None:
        self._queries: AiosqlQueries | None = None

    async def load_queries(self, path: str = "sql/", driver: str = "asyncpg") -> None:
        self._queries = aiosql.from_path(path, driver)

    async def get_user(
        self,
        connection: Connection,
        *,
        telegram_id: int,
    ) -> dict:
        response = await self._queries.get_user(
            connection,
            telegram_id=telegram_id,
        )
        return dict(response)
