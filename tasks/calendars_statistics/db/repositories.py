from collections.abc import Iterable
from datetime import date
from uuid import UUID

import asyncpg

from ..models.calendars import Calendar
from ..models.parsing_config import StatisticsParsingConfig
from .queries.builders import CalendarQueryBuilder


class CalendarRepository:
    def __init__(self, pool: asyncpg.Pool, queries: CalendarQueryBuilder):
        self._pool = pool
        self._queries = queries

    async def save_statistics(self, calendar_id: UUID, minutes: int, date: date) -> None:
        async with self._pool.acquire() as connection:
            await self._queries.save_statistics(
                connection=connection,
                calendar_id=calendar_id,
                minutes=minutes,
                date=date,
            )

    async def get_calendars_to_parse(self, timezones: Iterable[str], filter_date: date) -> list[Calendar]:
        async with self._pool.acquire() as connection:
            calendars = await self._queries.get_calendars_to_parse(
                connection=connection,
                timezones=timezones,
                filter_date=filter_date,
            )
            return [Calendar.model_validate(dict(calendar)) for calendar in calendars]

    async def get_statistics_parsing_config(self, user_id: UUID) -> StatisticsParsingConfig:
        async with self._pool.acquire() as connection:
            config_data = await self._queries.get_statistics_parsing_config(connection, user_id=user_id)
            return StatisticsParsingConfig.model_validate(config_data)
