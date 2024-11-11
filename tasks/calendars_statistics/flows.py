from prefect import flow


@flow(name="parse_calendars_statistics")
async def parse_calendars_statistics() -> None: ...
