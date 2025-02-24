from aiogram import Router

from pt_bot.settings import Settings

from .containers import CalendarContainer
from .routers.add_calendar import router as add_calendar_router
from .routers.disable_calendar import router as disable_calendar_router
from .routers.menu import router as menu_router


async def _get_container(settings: Settings) -> CalendarContainer:
    container = CalendarContainer()
    container.env.from_dict(settings.model_dump())
    # await container.init_resources()

    return container


async def get_router(settings: Settings) -> Router:
    _router = Router()
    _router.container = await _get_container(settings)
    _router.include_router(menu_router)
    _router.include_router(add_calendar_router)
    _router.include_router(disable_calendar_router)
    return _router
