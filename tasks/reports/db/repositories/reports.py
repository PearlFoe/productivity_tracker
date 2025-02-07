from collections.abc import AsyncIterator

import asyncpg

from ...models.flows_params import ReportFiler
from ...models.statistics import DailyStatistics, StatisticsExtremum
from ..queries.reports import ReportQueryBuilder


class ReportRepository:
    def __init__(self, pool: asyncpg.Pool, queries: ReportQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def get_user_statistics(
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

    async def get_statistics_extremums(self, filter: ReportFiler) -> StatisticsExtremum: ...
