from prefect import flow

from .models.flows_params import Calendar


@flow(name="parse_calendars_statistics")
async def parse_calendars_statistics(calendar: Calendar) -> None: ...
