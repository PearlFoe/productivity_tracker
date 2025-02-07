from uuid import UUID

import asyncpg

from ..queries.user import UserQueryBuilder


class UserRepository:
    def __init__(self, pool: asyncpg.Pool, queries: UserQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def get_user_telegram_id(self, user_id: UUID) -> int:
        async with self._pool.acquire() as connection:
            return await self._queries.get_user_telegram_id(connection, user_id=user_id)
