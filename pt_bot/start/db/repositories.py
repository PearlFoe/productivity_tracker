from uuid import UUID

import asyncpg

from ..errors import UserAlreadyExistsError
from .queries.builders import UserQueryBuilder


class UserRepository:
    def __init__(self, pool: asyncpg.Pool, queries: UserQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def check_user_exists(self, tg_id: int) -> bool:
        async with self._pool.acquire() as connection:
            user_id = await self._queries.get_user_id(
                connection=connection,
                tg_id=tg_id,
            )
            return bool(user_id)

    async def create_user(self, tg_id: int) -> UUID:
        async with self._pool.acquire() as connection:
            try:
                return await self._queries.create_user(
                    connection=connection,
                    tg_id=tg_id,
                )
            except asyncpg.exceptions.UniqueViolationError as e:
                raise UserAlreadyExistsError(tg_id=tg_id) from e

    async def create_statistics_parsing_config(self, user_id: UUID) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.create_statistics_parsing_config(connection, user_id=user_id)
