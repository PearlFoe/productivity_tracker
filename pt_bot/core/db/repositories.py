import asyncpg
from redis.asyncio import ConnectionPool, Redis

from pt_bot.core.models.user import User

from ..db.queries.builders import UserQueryBuilder


class UserRepository:
    def __init__(self, pool: asyncpg.Pool, queries: UserQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def get_data(self, telegram_id: int) -> User:
        async with self._pool.acquire() as connection:
            user_data = await self._queries.get_user(connection, telegram_id=telegram_id)
            return User.model_validate(user_data)


class UserCacheRepository:
    def __init__(self, pool: ConnectionPool, ttl: int, prefix: str = "user"):
        self._pool = pool
        self._ttl = ttl
        self._prefix = prefix

    def _build_key(self, telegram_id: int) -> str:
        return f"{self._prefix}__{telegram_id}"

    async def get_data(self, telegram_id: int) -> User | None:
        async with Redis.from_pool(self._pool) as connection:
            data = await connection.get(self._build_key(telegram_id))
            if not data:
                return None
            return User.model_validate_json(data)

    async def save_data(self, user: User) -> None:
        async with Redis.from_pool(self._pool) as connection:
            await connection.setex(
                name=self._build_key(user.telegram_id),
                value=user.model_dump_json(),
                time=self._ttl,
            )
