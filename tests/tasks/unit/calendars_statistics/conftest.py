import datetime
from uuid import uuid4

import pytest

from tasks.calendars_statistics.constants import GOOGLE_API_DATETIME_RESPONSE_FORMAT
from tasks.calendars_statistics.containers import CalendarsStatisticsContainer
from tasks.calendars_statistics.models.calendars import Calendar
from tasks.calendars_statistics.models.client.events import Event
from tasks.calendars_statistics.services.statistics import StatisticsService
from tasks.settings import Settings

from .mocks.clients import GoogleCalendarAPIClientMock
from .mocks.repositories import CalendarRepository


@pytest.fixture
def calendars_statistics_container() -> CalendarsStatisticsContainer:
    settings = Settings()
    container = CalendarsStatisticsContainer()
    container.env.from_dict(settings.model_dump())

    container.google_api_client.override(GoogleCalendarAPIClientMock())
    container.calendar_repository.override(CalendarRepository())

    return container


@pytest.fixture
def statistics_service(calendars_statistics_container: CalendarsStatisticsContainer) -> StatisticsService:
    return calendars_statistics_container.statistics_service()


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


@pytest.fixture
def calendar_events() -> list[Event]:
    def format_dt(dt: datetime.datetime) -> str:
        tz_minutes = ":00"
        return dt.strftime(GOOGLE_API_DATETIME_RESPONSE_FORMAT) + tz_minutes

    tz = datetime.UTC
    now = datetime.datetime.now(tz)
    return [
        Event(
            id=str(uuid4()),
            summary="Test event title",
            start={"dateTime": format_dt(now - datetime.timedelta(hours=1))},
            end={"dateTime": format_dt(now)},
        ),
    ]
