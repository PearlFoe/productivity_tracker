from collections.abc import AsyncIterator

from ..models.flows_params import ReportFiler
from ..models.statistics import DailyStatistics


class StatisticsRepository:
    def __init__(self): ...

    async def get_user_statistics(
        self,
        filter: ReportFiler,
    ) -> AsyncIterator[tuple[str, list[DailyStatistics]]]: ...
