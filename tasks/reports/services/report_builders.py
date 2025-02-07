import asyncio
from collections.abc import AsyncIterator, Iterable
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

from ..db.repositories.reports import ReportRepository
from ..models.flows_params import ReportFiler
from ..models.statistics import DailyStatistics
from .builders import UserReportBuilder
from .charts.chart_sets import BaseChartSet


class ReportBuildingService:
    def __init__(
        self,
        statistics: ReportRepository,
        pool: ThreadPoolExecutor,
    ):
        self._statistics = statistics
        self._pool = pool

    async def _build_report(
        self,
        statistics: AsyncIterator[tuple[str, Iterable[DailyStatistics]]],
        dates: Iterable[date],
        chart_set: BaseChartSet,
    ) -> str:
        report = UserReportBuilder(chart_set)
        loop = asyncio.get_running_loop()

        async for calendar_name, calendar_statistics in statistics:
            await loop.run_in_executor(
                self._pool,
                report.add_calendar_statistics,
                calendar_name,
                calendar_statistics,
            )
        await loop.run_in_executor(self._pool, report.add_labels, dates)

        return await loop.run_in_executor(self._pool, report.build_html)

    @staticmethod
    def _dates_range(start: date, end: date) -> list[date]:
        return [start + timedelta(days) for days in range((end - start).days)]

    async def build_html(self, filter: ReportFiler, chart_set: BaseChartSet) -> str:
        statistics = self._statistics.get_user_statistics(filter)
        dates = self._dates_range(filter.start, filter.end)
        return await self._build_report(statistics, dates, chart_set)
