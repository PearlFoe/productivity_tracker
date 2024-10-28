from aiogram.types.user import User

class UserService:
    def __init__(self) -> None:
        pass

    async def user_exists(self, user: User) -> bool:
        ...

    async def create_new_user(self, user: User) -> None:
        ...
