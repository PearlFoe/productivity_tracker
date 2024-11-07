import pytest

from bot.calendars.containers import CalendarContainer
from bot.calendars.models.calendars import Calendar
from bot.calendars.services.calendars import CalendarService
from bot.settings import Settings

from .mocks import clients, repositories


@pytest.fixture
async def calendar_container(settings: Settings) -> CalendarContainer:
    container = CalendarContainer()
    container.env.from_dict(settings.model_dump())

    container.google_calendar_client.override(clients.GoogleCalendarAPIClientMock())
    container.calendar_repository.override(repositories.CalendarRepoositoryMock())

    return container


@pytest.fixture
def calendar_service(calendar_container: CalendarContainer) -> CalendarService:
    return calendar_container.calendar_service()


@pytest.fixture
def google_id() -> str:
    return "some_test_id@group.calendar.google.com"


@pytest.fixture
def calendar(google_id: str) -> Calendar:
    return Calendar(
        google_id=google_id,
        name="test_calendar_name",
        timezone="Etc/UTC",
    )
