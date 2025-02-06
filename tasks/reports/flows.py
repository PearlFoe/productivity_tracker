from prefect import flow

from .models.flows_params import ReportFiler


@flow(name="build_weekly_report")
async def build_weekly_report(filter: ReportFiler) -> None: ...
