from src.start.errors import UserAlreadyExistsError


class UserRepositoryMock:
    def __init__(self, pool = None, queries = None):
        self._db = {}

    async def check_user_exists(self, tg_id: int) -> bool:
        return tg_id in self._db

    async def create_user(self, tg_id: int) -> None:
        if tg_id in self._db:
            raise UserAlreadyExistsError(tg_id=tg_id)

        self._db[tg_id] = tg_id

