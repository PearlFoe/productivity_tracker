from prefect import flow

from tasks.settings import Settings

from .containers import ReportContainer
from .models.flows_params import ReportFiler
from .services.charts.chart_sets import UserReportChartSet
from .services.distribution import ReportDistributionService
from .services.report_builders import ReportBuildingService

SETTINGS = Settings()
CONTAINER = ReportContainer()
CONTAINER.env.from_dict(SETTINGS.model_dump())


@flow(name="build_report")
async def build_report(filter: ReportFiler) -> None:
    report_builder: ReportBuildingService = await CONTAINER.report_building_service()
    report_distributor: ReportDistributionService = await CONTAINER.report_distribution_service()

    report = await report_builder.build_html(
        filter=filter,
        chart_set=UserReportChartSet(),
    )
    await report_distributor.send_report(
        user_id=filter.user_id,
        report=report,
    )


@flow(name="schedule_report_building")
async def schedule_report_building() -> None:
    report_distributor: ReportDistributionService = await CONTAINER.report_distribution_service()

    start, end = report_distributor.get_weekly_report_dates()
    users = await report_distributor.get_users_to_send_report()

    for user_id in users:
        filter = ReportFiler(
            user_id=user_id,
            start=start,
            end=end,
        )

        await build_report(filter)
