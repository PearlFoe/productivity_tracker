import pytest
from aiogram.types import User

from src.settings import Settings
from src.start.containers import StartContainer
from src.start.services.users import UserService

from .mocks.start.repositories import UserRepositoryMock


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
async def start_container(settings: Settings):
    container = StartContainer()
    container.env.from_dict(settings.model_dump())

    container.user_repository.override(UserRepositoryMock())

    return container


@pytest.fixture
def user_service(start_container: StartContainer) -> UserService:
    return start_container.user_service()


@pytest.fixture
def user() -> User:
    return User(id=42, is_bot=False, first_name="Test")
