from prefect import flow

from tasks.settings import Settings

from .containers import CalendarsStatisticsContainer
from .models.flows_params import StatisticsFilters
from .services.statistics import StatisticsService

SETTINGS = Settings()
CONTAINER = CalendarsStatisticsContainer()
CONTAINER.env.from_dict(SETTINGS.model_dump())


@flow(name="parse_calendars_statistics")
async def parse_calendars_statistics(
    filters: StatisticsFilters,
) -> None:
    statistics_service: StatisticsService = await CONTAINER.statistics_service()
    await statistics_service.parse_statistics(filters)


@flow(name="schedule_calendars_statistics_parsing", log_prints=True)
async def schedule_calendars_statistics_parsing() -> None:
    statistics_service: StatisticsService = await CONTAINER.statistics_service()

    calendars_to_parse = await statistics_service.get_calendars_to_parse()
    for calendar in calendars_to_parse:
        start, end = statistics_service.parsing_interval(calendar.timezone)
        filters = StatisticsFilters(
            calendar_id=calendar.id,
            calendar_google_id=calendar.google_id,
            start=start,
            end=end,
        )
        await parse_calendars_statistics(filters=filters.model_dump())
