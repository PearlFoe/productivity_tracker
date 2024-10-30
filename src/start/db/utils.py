from typing import Protocol
from collections.abc import AsyncIterator

from asyncpg import create_pool, Connection
from pydantic import networks


class _LoadableQueryBuilder(Protocol):
    async def load_queries(self, path: str, driver: str) -> None: ...


async def load_queries(
    builder: _LoadableQueryBuilder, path: str = "sql/", driver: str = "asyncpg"
) -> _LoadableQueryBuilder:
    await builder.load_queries(path, driver)
    return builder


async def init_db_connection_pool(dsn: networks.PostgresDsn) -> AsyncIterator[Connection]:
    async with create_pool(dsn=str(dsn)) as pool:
        yield pool
