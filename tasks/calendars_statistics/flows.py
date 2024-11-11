from prefect import flow

from tasks.settings import Settings

from .containers import CalendarsStatisticsContainer
from .models.flows_params import StatisticsFilters
from .services.statistics import StatisticsService

CONTAINER = CalendarsStatisticsContainer()
CONTAINER.env.from_dict(Settings().model_dump())


@flow(name="parse_calendars_statistics")
async def parse_calendars_statistics(
    filters: StatisticsFilters,
) -> None:
    statistics_service: StatisticsService = await CONTAINER.statistics_service()
    await statistics_service.parse_statistics(filters)
