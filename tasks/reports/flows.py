from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from prefect import flow

from tasks.settings import Settings

from .containers import ReportContainer
from .models.flows_params import ReportFiler
from .services.chart_sets import UserReportChartSet
from .services.report_builders import ReportBuildingService

SETTINGS = Settings()
CONTAINER = ReportContainer()
CONTAINER.env.from_dict(SETTINGS.model_dump())


@flow(name="build_weekly_report")
async def build_weekly_report(filter: ReportFiler) -> None:
    report_builder: ReportBuildingService = await CONTAINER.report_building_service()

    report = await report_builder.build_html(
        filter=filter,
        chart_set=UserReportChartSet(),
    )

    bot = Bot("7099637546:AAE4DVfcm1AaUYM0T9QG8vuA_pRsopXkp1U")
    await bot.send_document(659797592, BufferedInputFile(file=report.encode(), filename="report.html"))
