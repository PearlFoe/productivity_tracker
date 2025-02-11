import datetime
from uuid import UUID

from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile

from ..db.repositories.user import UserRepository


class ReportDistributionService:
    def __init__(self, bot: Bot, user: UserRepository) -> None:
        self._bot = bot
        self._user = user

    async def send_report(self, user_id: UUID, report: str, file_name: str = "report.html") -> None:
        user_tg_id = await self._user.get_user_telegram_id(user_id)
        file = BufferedInputFile(file=report.encode(), filename=file_name)

        await self._bot.send_document(user_tg_id, file)

    def get_weekly_report_dates(self) -> tuple[datetime.date, datetime.date]:
        today = datetime.datetime.now(tz=datetime.UTC).date()
        return today - datetime.timedelta(days=7), today

    async def get_users_to_send_report(self) -> list[UUID]:
        return await self._user.get_users_to_send_report()
