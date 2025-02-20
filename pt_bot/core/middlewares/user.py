from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from pt_bot.core.models.user import User

from ...core.containers import CoreContainer
from ..db.repositories import UserCacheRepository, UserRepository


class UserInjector(BaseMiddleware):
    @inject
    def __init__(
        self,
        storage: UserRepository = Provide[CoreContainer.user_repository],
        cache: UserCacheRepository = Provide[CoreContainer.user_cache_repository],
    ):
        self._storage = storage
        self._cache = cache

    async def _get_user(self, telegram_id: int) -> User:
        user = await self._cache.get_data(telegram_id)

        if not user:
            user = await self._storage.get_data(telegram_id)
            await self._cache.save_data(user)

        return user

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_param = handler.__annotations__.get("user")

        if not user_param:
            return await handler(event, data)

        data["user"] = self._get_user(telegram_id=event.from_user.id)

        return await handler(event, data)
