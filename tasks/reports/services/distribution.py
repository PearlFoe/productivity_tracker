import datetime
from uuid import UUID

from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile

from ..db.repositories.reports import ReportRepository
from ..db.repositories.user import UserRepository
from ..models.reports import Report


class ReportDistributionService:
    def __init__(self, bot: Bot, user: UserRepository, report: ReportRepository) -> None:
        self._bot = bot
        self._user = user
        self._report = report

    async def send_report(self, report: Report) -> None:
        user_tg_id = await self._user.get_user_telegram_id(report.user_id)
        file = BufferedInputFile(file=report.data.encode(), filename=report.file_name)

        await self._bot.send_document(user_tg_id, file)
        await self._report.save_report_info(report)

    def get_weekly_report_dates(self) -> tuple[datetime.date, datetime.date]:
        today = datetime.datetime.now(tz=datetime.UTC).date()
        return today - datetime.timedelta(days=7), today

    async def get_users_to_send_report(self) -> list[tuple[UUID, UUID]]:
        return await self._user.get_users_to_send_report()
