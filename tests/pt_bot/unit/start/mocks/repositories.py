from uuid import UUID, uuid4

from pt_bot.start.errors import UserAlreadyExistsError


class UserRepositoryMock:
    def __init__(self, pool=None, queries=None):
        self._db = {
            "users": {},
            "parsing_config": {},
        }

    async def check_user_exists(self, tg_id: int) -> bool:
        return tg_id in self._db["users"]

    async def create_user(self, tg_id: int) -> UUID:
        if tg_id in self._db["users"]:
            raise UserAlreadyExistsError(tg_id=tg_id)

        user_id = uuid4()
        self._db["users"][tg_id] = user_id
        return user_id

    async def create_statistics_parsing_config(self, user_id: UUID) -> None:
        config_id = uuid4()
        self._db["parsing_config"][user_id] = config_id
