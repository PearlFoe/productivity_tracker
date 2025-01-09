import datetime

import pytest
from freezegun import freeze_time

from tasks.calendars_statistics.models.calendars import Calendar
from tasks.calendars_statistics.models.client.events import Event
from tasks.calendars_statistics.services.statistics import StatisticsService


class TestStatisticsService:
    @pytest.mark.parametrize(
        "tz",
        [
            datetime.UTC,
        ],
    )
    def test_parsing_interval_generation(
        self,
        tz: str,
        statistics_service: StatisticsService,
    ):
        start_dt, end_dt = statistics_service.parsing_interval(tz)
        assert start_dt < end_dt

    def test_parsing_interval_generation__default_timezone(
        self,
        statistics_service: StatisticsService,
    ):
        start_dt, end_dt = statistics_service.parsing_interval()
        assert start_dt < end_dt

    @freeze_time("2025-01-01 02:00:00")
    def test_timezones_to_parse(self, statistics_service: StatisticsService):
        available_timezones = {
            "America/Godthab",
            "Atlantic/South_Georgia",
            "Brazil/DeNoronha",
            "Etc/GMT+1",
            "Atlantic/Azores",
            "America/Scoresbysund",
            "Atlantic/Cape_Verde",
            "Etc/GMT+2",
            "America/Nuuk",
            "America/Noronha",
        }
        timezones_to_parse = statistics_service.timezones_to_parse()
        assert available_timezones == set(timezones_to_parse)

    @freeze_time("2025-01-01 00:00:00")
    async def test_get_calendars_to_parse(
        self, statistics_service: StatisticsService, calendar: Calendar, calendar_events: list[Event]
    ):
        statistics_service._calendar._calendar._db["calendars"][calendar.id] = calendar
        statistics_service._client._db[calendar.id] = calendar_events

        calendars = await statistics_service.get_calendars_to_parse()

        assert any(calendar.id == c.id for c in calendars)
