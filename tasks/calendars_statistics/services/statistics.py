import datetime
from zoneinfo import ZoneInfo, available_timezones

from tenacity import RetryError

from ..models.calendars import Calendar
from ..models.client.events import Event
from ..models.flows_params import StatisticsFilters
from .calendars import CalendarService
from .clients import GoogleCalendarAPIClient


class StatisticsService:
    def __init__(self, calendar_service: CalendarService, api_client: GoogleCalendarAPIClient) -> None:
        self._calendar = calendar_service
        self._client = api_client

    def count_total_minutes(self, events: list[Event], start: datetime, end: datetime) -> int:
        minutes = 0

        for event in events:
            event_start = event.start.datetime or event.start.date
            period_start = start if event.start.datetime else start.date()
            event_start = event_start if event_start >= period_start else period_start  # lates start

            event_end = event.end.datetime or event.end.date
            period_end = end if event.end.datetime else end.date()
            event_end = event_end if event_end <= period_end else period_end  # earlies end

            minutes += (event_end - event_start).total_seconds() // 60

        return minutes

    async def parse_statistics(self, filters: StatisticsFilters) -> None:
        try:
            events = await self._client.events(
                calendar_id=filters.calendar_google_id,
                start=filters.start,
                end=filters.end,
            )
        except RetryError:
            events = []

        await self._calendar.save_calendar_statistics(
            calendar_id=filters.calendar_id,
            minutes=self.count_total_minutes(events, filters.start, filters.end),
            date=filters.start.date(),
        )

    def timezones_to_parse(self) -> list[str]:
        timezones_to_parse = []
        for tz_name in available_timezones():
            now = datetime.datetime.now(ZoneInfo(tz_name))
            if 0 <= now.hour <= 1:
                timezones_to_parse.append(tz_name)

        return timezones_to_parse

    def parsing_interval(self, tz: str = "Etc/UTC") -> tuple[datetime.datetime, datetime.datetime]:
        tz = ZoneInfo(tz)
        return (
            datetime.datetime.now(tz) - datetime.timedelta(days=1),
            datetime.datetime.now(tz),
        )

    async def get_calendars_to_parse(self) -> list[Calendar]:
        timezones_to_parse = self.timezones_to_parse()
        if not timezones_to_parse:
            return []

        tz = timezones_to_parse[0]
        filter_dt, _ = self.parsing_interval(tz)

        return await self._calendar.get_calendars_to_parse(
            timezones=timezones_to_parse,
            filter_date=filter_dt.date(),
        )
