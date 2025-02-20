from collections.abc import AsyncIterator
from typing import Protocol

from asyncpg import Connection, create_pool
from pydantic import networks
from redis.asyncio import ConnectionPool, Redis


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


async def redis_pool(redis_dsn: str) -> AsyncIterator[ConnectionPool]:
    pool = ConnectionPool.from_url(redis_dsn)
    yield pool
    await pool.aclose()


async def redis_session(pool: ConnectionPool) -> AsyncIterator[Redis]:
    session = Redis.from_pool(pool)
    yield session
    await session.close()
