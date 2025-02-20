from ..db.repositories import UserCacheRepository, UserRepository
from ..models.user import User


class UserService:
    def __init__(
        self,
        storage: UserRepository,
        cache: UserCacheRepository,
    ):
        self._storage = storage
        self._cache = cache

    async def get_user(self, telegram_id: int) -> tuple[bool, User]:
        cached = True
        user = await self._cache.get_data(telegram_id)

        if not user:
            cached = False
            user = await self._storage.get_data(telegram_id)

        return cached, user

    async def cache_user(self, user: User) -> None:
        await self._cache.save_data(user)
