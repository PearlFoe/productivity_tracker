from aiogram.types import User

from src.start.services.users import UserService


class TestUserService:
    async def test_check_user_exists__no_user(self, user_service: UserService, user: User):
        exists = await user_service.user_exists(user)
        assert not exists

    async def test_check_user_exists(self, user_service: UserService, user: User):
        user_service._user._db[user.id] = user.id
        exists = await user_service.user_exists(user)
        assert exists

    async def test_create_new_user(self, user_service: UserService, user: User):
        await user_service.create_new_user(user)
        exists = await user_service.user_exists(user)
        assert exists

    async def test_create_new_user__user_duplicate(self, user_service: UserService, user: User):
        await user_service.create_new_user(user)
        await user_service.create_new_user(user)
        exists = await user_service.user_exists(user)

        assert exists
