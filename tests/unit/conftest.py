import pytest
from aiogram.types import User

from bot.settings import Settings


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def user() -> User:
    return User(id=42, is_bot=False, first_name="Test")
