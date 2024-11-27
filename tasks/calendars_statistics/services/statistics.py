from ..models.client.events import Event
from ..models.flows_params import StatisticsFilters
from .calendars import CalendarService
from .clients import GoogleCalendarAPIClient


class StatisticsService:
    def __init__(self, calendar_service: CalendarService, api_client: GoogleCalendarAPIClient) -> None:
        self._calendar = calendar_service
        self._client = api_client

    @staticmethod
    def _count_total_minutes(events: list[Event]) -> int:
        return sum((event.end - event.start).seconds // 60 for event in events)

    async def parse_statistics(self, filters: StatisticsFilters) -> None:
        events = await self._client.events(
            calendar_id=filters.calendar_google_id,
            start=filters.start,
            end=filters.end,
        )
        await self._calendar.save_calendar_statistics(
            calendar_id=filters.calendar_id,
            minutes=self._count_total_minutes(events),
            date=filters.start.date(),
        )
