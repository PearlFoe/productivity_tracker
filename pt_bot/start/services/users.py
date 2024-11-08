import contextlib

from aiogram.types.user import User

from ..db.repositories import UserRepository
from ..errors import UserAlreadyExistsError


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user = user_repository

    async def user_exists(self, user: User) -> bool:
        return await self._user.check_user_exists(user.id)

    async def create_new_user(self, user: User) -> None:
        with contextlib.suppress(UserAlreadyExistsError):
            await self._user.create_user(user.id)
