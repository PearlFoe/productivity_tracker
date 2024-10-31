import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from src.settings import Settings
from src.bot.containers import BotContainer
from src.bot.commands import COMMANDS
from src.start import get_router as get_start_router
from src.calendars import get_router as get_calendar_router


async def _include_routers(dp: Dispatcher, settings: Settings) -> None:
    routers_getters = (
        get_start_router,
        get_calendar_router,
    )

    for getter in routers_getters:
        router = await getter(settings)
        dp.include_router(router)


# TODO: Add containers resources startup and shutdown


async def main() -> None:
    settings = Settings()
    container = BotContainer()
    container.env.from_dict(settings.model_dump())
    await container.init_resources()

    bot = Bot(token=settings.bot_api_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=await container.redis_storage())

    await bot.set_my_commands(COMMANDS)

    await _include_routers(dp, settings)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await container.shutdown_resources()


if __name__ == "__main__":
    asyncio.run(main())
