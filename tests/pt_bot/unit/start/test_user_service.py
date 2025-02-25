from aiogram.types import User

from pt_bot.start.services.users import UserService


class TestUserService:
    async def test_check_user_exists__no_user(self, user_service: UserService, telegram_user: User):
        user_service._user._db["users"].clear()
        assert not await user_service.user_exists(telegram_user)

    async def test_check_user_exists(self, user_service: UserService, telegram_user: User):
        user_service._user._db["users"][telegram_user.id] = telegram_user.id
        assert await user_service.user_exists(telegram_user)

    async def test_create_new_user(self, user_service: UserService, telegram_user: User):
        user_service._user._db["users"].clear()
        user_service._user._db["parsing_config"].clear()

        await user_service.create_new_user(telegram_user)

        assert user_service._user._db["users"]
        assert user_service._user._db["parsing_config"]

    async def test_create_new_user__user_duplicate(self, user_service: UserService, telegram_user: User):
        user_service._user._db["users"].clear()
        user_service._user._db["parsing_config"].clear()

        await user_service.create_new_user(telegram_user)
        await user_service.create_new_user(telegram_user)

        assert await user_service.user_exists(telegram_user)
