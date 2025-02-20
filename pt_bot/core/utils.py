from collections.abc import Callable
from functools import wraps
from typing import Any

from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from .containers import CoreContainer
from .models.user import User
from .services.user import UserService


def _injection_expected(f: Callable) -> bool:
    user = f.__annotations__.get("user")
    return bool(user and issubclass(user, User))


def inject_user(f: Callable) -> Callable:
    @wraps(f)
    @inject
    async def wrapper(
        *args: tuple,
        user_service: UserService = Provide[CoreContainer.user_service],
        **kwargs: dict,
    ) -> Any:
        # IMPORTANT
        # To make this injection work you have to add every module,
        # where this decorator is used, into CoreContainer.wiring_config.
        if not _injection_expected(f):
            return await f(*args, **kwargs)

        message: Message = args[0]  # type: ignore
        user_telegram_id = message.from_user.id

        cached, user = await user_service.get_user(user_telegram_id)
        if not cached:
            await user_service.cache_user(user)

        kwargs["user"] = user  # type: ignore
        return await f(*args, **kwargs)

    return wrapper
