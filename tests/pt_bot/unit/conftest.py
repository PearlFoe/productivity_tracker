from uuid import uuid4

import pytest
from aiogram.types import User as TelegramUser

from pt_bot.core.models.user import User
from pt_bot.settings import Settings


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def telegram_user() -> TelegramUser:
    return TelegramUser(id=42, is_bot=False, first_name="Test")


@pytest.fixture
def user(telegram_user: TelegramUser) -> User:
    return User(id=uuid4(), telegram_id=telegram_user.id)
