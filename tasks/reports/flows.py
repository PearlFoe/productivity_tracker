from prefect import flow

from tasks.settings import Settings

from .containers import ReportContainer
from .models.flows_params import ReportFiler
from .services.chart_sets import UserReportChartSet
from .services.distribution import ReportDistributionService
from .services.report_builders import ReportBuildingService

SETTINGS = Settings()
CONTAINER = ReportContainer()
CONTAINER.env.from_dict(SETTINGS.model_dump())


@flow(name="build_weekly_report")
async def build_weekly_report(filter: ReportFiler) -> None:
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
