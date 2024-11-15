from prefect import flow

from tasks.calendars_statistics.containers import CalendarsStatisticsContainer
from tasks.core.wiring import wrap_injected
from tasks.settings import Settings

_settigs = Settings()
_container = CalendarsStatisticsContainer()
_container.env.from_dict(_settigs.model_dump())
_container.wire()

from .flows import parse_calendars_statistics

parse_calendars_statistics = flow(
    wrap_injected(parse_calendars_statistics),
    name="parse_calendars_statistics",
)
