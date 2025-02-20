from collections.abc import AsyncIterator

import asyncpg

from tasks.reports.models.flows_params import ReportFiler
from tasks.reports.models.reports import Report
from tasks.reports.models.statistics import DailyStatistics, StatisticsExtremum

from ..queries.reports import ReportQueryBuilder


class ReportRepository:
    def __init__(self, pool: asyncpg.Pool, queries: ReportQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def get_statistics(
        self,
        filter: ReportFiler,
    ) -> AsyncIterator[tuple[str, list[DailyStatistics]]]:
        async with self._pool.acquire() as connection:
            calendars = await self._queries.get_user_calendars(connection, user_id=filter.user_id)

            for calendar_name in calendars:
                data = await self._queries.get_calendar_statistics(
                    connection,
                    calendar_name=calendar_name,
                    start=filter.start,
                    end=filter.end,
                )
                statistics = [DailyStatistics.model_validate(d) for d in data]
                yield calendar_name, statistics

    async def get_statistics_extremums(self, filter: ReportFiler) -> StatisticsExtremum:
        async with self._pool.acquire() as connection:
            data = await self._queries.get_statistics_extremums(
                connection=connection,
                user_id=filter.user_id,
                start=filter.start,
                end=filter.end,
            )
            return StatisticsExtremum.model_validate(data)

    async def save_report_info(self, report: Report) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.save_report_info(
                connection,
                user_id=report.user_id,
                schedule_id=report.schedule_id,
                name=report.name,
            )
