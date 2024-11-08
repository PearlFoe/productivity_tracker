import pytest

from pt_bot.settings import Settings
from pt_bot.start.containers import StartContainer
from pt_bot.start.services.users import UserService

from .mocks.repositories import UserRepositoryMock


@pytest.fixture
async def start_container(settings: Settings) -> StartContainer:
    container = StartContainer()
    container.env.from_dict(settings.model_dump())

    container.user_repository.override(UserRepositoryMock())

    return container


@pytest.fixture
def user_service(start_container: StartContainer) -> UserService:
    return start_container.user_service()
