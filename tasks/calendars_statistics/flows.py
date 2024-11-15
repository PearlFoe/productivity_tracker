from typing import Any

from dependency_injector.wiring import Provide, inject

from .containers import CalendarsStatisticsContainer
from .models.flows_params import StatisticsFilters
from .services.statistics import StatisticsService


@inject
async def parse_calendars_statistics(
    filters: StatisticsFilters,
    statistics_service: StatisticsService | Any = Provide[CalendarsStatisticsContainer.statistics_service],
) -> None:
    await statistics_service.parse_statistics(filters)
