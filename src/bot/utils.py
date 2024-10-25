from collections.abc import AsyncIterator

from redis.asyncio import Redis, ConnectionPool


async def redis_pool(redis_dsn: str) -> AsyncIterator[ConnectionPool]:
    pool = ConnectionPool.from_url(redis_dsn)
    yield pool
    await pool.aclose()


async def redis_session(pool: ConnectionPool) -> AsyncIterator[Redis]:
    session = Redis.from_pool(pool)
    yield session
    await session.close()

