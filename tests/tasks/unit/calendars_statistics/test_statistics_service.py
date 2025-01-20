import datetime
from collections.abc import Iterable

import pytest
from freezegun import freeze_time

from tasks.calendars_statistics.models.calendars import Calendar
from tasks.calendars_statistics.models.client.events import Event
from tasks.calendars_statistics.services.statistics import StatisticsService

from .data.events import (
    SINGE_HOUR_EVENT,
    SINGE_HOUR_EVENT__ENDS_NEXT_DAY,
    SINGLE_ALL_DAY_EVENT,
    TWO_ALL_DAY_EVENTS,
    TWO_ALL_DAY_EVENTS__SAME_DAY,
    TWO_HOUR_EVENTS,
    TWO_HOUR_EVENTS__SAME_HOUR,
)


class TestStatisticsService:
    @pytest.mark.parametrize(
        "tz",
        [
            "Etc/UTC",
            "Etc/GMT+1",
            "Etc/GMT+2",
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

    @pytest.mark.parametrize(
        ("events", "expected_minutes", "start", "end"),
        [
            (
                [],
                0,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                SINGE_HOUR_EVENT,
                60,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                TWO_HOUR_EVENTS,
                120,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                SINGLE_ALL_DAY_EVENT,
                1440,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                TWO_ALL_DAY_EVENTS,
                2880,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=3, tzinfo=datetime.UTC),
            ),
            (
                TWO_HOUR_EVENTS__SAME_HOUR,
                120,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                TWO_ALL_DAY_EVENTS__SAME_DAY,
                2880,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                SINGE_HOUR_EVENT__ENDS_NEXT_DAY,
                30,
                datetime.datetime(year=2025, month=1, day=1, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
            ),
            (
                SINGE_HOUR_EVENT__ENDS_NEXT_DAY,
                30,
                datetime.datetime(year=2025, month=1, day=2, tzinfo=datetime.UTC),
                datetime.datetime(year=2025, month=1, day=3, tzinfo=datetime.UTC),
            ),
        ],
    )
    async def test_count_total_minutes(
        self,
        events: Iterable[Event],
        expected_minutes: int,
        start: datetime.datetime,
        end: datetime.datetime,
        statistics_service: StatisticsService,
    ):
        result_minutes = statistics_service.count_total_minutes(events, start, end)
        assert expected_minutes == result_minutes
