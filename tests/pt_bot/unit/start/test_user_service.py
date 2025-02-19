from aiogram.types import User

from pt_bot.start.services.users import UserService


class TestUserService:
    async def test_check_user_exists__no_user(self, user_service: UserService, telegram_user: User):
        exists = await user_service.user_exists(telegram_user)
        assert not exists

    async def test_check_user_exists(self, user_service: UserService, telegram_user: User):
        user_service._user._db[telegram_user.id] = telegram_user.id
        exists = await user_service.user_exists(telegram_user)
        assert exists

    async def test_create_new_user(self, user_service: UserService, telegram_user: User):
        await user_service.create_new_user(telegram_user)
        exists = await user_service.user_exists(telegram_user)
        assert exists

    async def test_create_new_user__user_duplicate(self, user_service: UserService, telegram_user: User):
        await user_service.create_new_user(telegram_user)
        await user_service.create_new_user(telegram_user)
        exists = await user_service.user_exists(telegram_user)

        assert exists
