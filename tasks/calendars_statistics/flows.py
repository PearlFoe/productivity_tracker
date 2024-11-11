from dependency_injector.wiring import Provide, inject
from prefect import flow

from .containers import CalendarsStatisticsContainer
from .models.flows_params import StatisticsFilters
from .services.statistics import StatisticsService


@flow(name="parse_calendars_statistics")
@inject
async def parse_calendars_statistics(
    filters: StatisticsFilters,
    statistics_service: StatisticsService = Provide[CalendarsStatisticsContainer.statistics_service],
) -> None:
    await statistics_service.parse_statistics(filters)
